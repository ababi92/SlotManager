/*
 * Copyright (c) 2007, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

/**

 */

#include "contiki.h"
#include "net/rime/rime.h"

#include <stdio.h>
#include <string.h>
#include <avr/interrupt.h>
#include <util/delay.h>

/*---------------------------------------------------------------------------*/
PROCESS(unicast_process, "Unicast process");
PROCESS(broadcast_process, "Broadcast process");
AUTOSTART_PROCESSES(&unicast_process, &broadcast_process);
/*---------------------------------------------------------------------------*/

static volatile int state = 1;
static volatile int winner = 0;
static volatile int counter = 1;
static volatile int car1 = 0;
static volatile int car2 = 0;
static struct etimer et2;

// Idea afegir funcio enable_interrupts disable_interrupts
// Idea afegir un estat initial que esperi el reset per a començar a enviar advertisements

static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from){
  printf("Broadcast message received: '%s', state: %d \n", (char *)packetbuf_dataptr(), state);
  if(strcmp("READY", (char *)packetbuf_dataptr()) == 0){
    state = 1;
    counter = 1;
    printf("READY received\n");
    EICRA &= ~(1 << ISC01);   // Disable external interrupts
    EICRA &= ~(1 << ISC11);
    EIMSK &= ~(1 << INT0);
    EIMSK &= ~(1 << INT1);
  }
  else if(strcmp("START", (char *)packetbuf_dataptr()) == 0){
    if ( (state == 1) || (state == 3) || (state == 4) ){
      state = 2;
      EICRA &= ~(1 << ISC01);   // Disable external interrupts
      EICRA &= ~(1 << ISC11);
      EIMSK &= ~(1 << INT0);
      EIMSK &= ~(1 << INT1);
    };
    printf("START received\n");
  }

  else if(strcmp("WIN 1", (char *)packetbuf_dataptr()) == 0){
    if (state == 3){
      state = 4;
      PORTF &= ~(1 << PF3);   // IDEA: Que els leds no s'encenguin aqui sino al modul
      PORTF |= (1 << PF2);    
      EICRA &= ~(1 << ISC01);   // Disable external interrupts
      EICRA &= ~(1 << ISC11);
      EIMSK &= ~(1 << INT0);
      EIMSK &= ~(1 << INT1);
    };
    printf("WIN 1 received\n");
  }
  
  else if(strcmp("WIN 2", (char *)packetbuf_dataptr()) == 0){
    if (state == 3){
      state = 4;
      PORTF &= ~(1 << PF2);
      PORTF |= (1 << PF3);
      EICRA &= ~(1 << ISC01);   // Disable external interrupts
      EICRA &= ~(1 << ISC11);
      EIMSK &= ~(1 << INT0);
      EIMSK &= ~(1 << INT1);
    };
    printf("WIN 2 received\n");
  }
  else
    printf("Invalid msg received");
}

static void
unicast_recv(struct unicast_conn *c, const linkaddr_t *from)
{
printf("unicast message received from %d.%d: '%s'\n",
	 from->u8[0], from->u8[1], (char *)packetbuf_dataptr());
}

static const struct broadcast_callbacks broadcast_callbacks = {broadcast_recv};
static struct broadcast_conn bc;

static const struct unicast_callbacks unicast_callbacks = {unicast_recv};
static struct unicast_conn uc;
static const linkaddr_t addr = {1, 1, 1, 1, 1, 1, 1, 1};  


PROCESS_THREAD(broadcast_process, ev, data)
{
  static struct etimer et;
  
  PROCESS_EXITHANDLER(broadcast_close(&bc);)
    
  PROCESS_BEGIN();

  DDRD &= ~(1 << DDD0);
  DDRD &= ~(1 << DDD1);
  PORTD |= ((1 << PD0) | (1 << PD1)); // External interrupts 
  
  DDRF |= (1 << DDF2) | (1 << DDF3);  // LEDs
  
  sei();
  EICRA |= ((1 << ISC01) | (1 << ISC11));   // External interrupts
  EIMSK |= ((1 << INT0) | (1 << INT1));
  
  broadcast_open(&bc, 129, &broadcast_callbacks);
  
  while(1) {
    etimer_set(&et, CLOCK_SECOND);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
  }
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(unicast_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&uc);)  
  PROCESS_BEGIN();
  unicast_open(&uc, 146, &unicast_callbacks);
  static struct etimer et;
  
  while(state == 0) {
        
    etimer_set(&et, CLOCK_SECOND);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
    
    packetbuf_copyfrom("Advrt", 6);
    printf("Adv. sent\n");
    
    if(!linkaddr_cmp(&addr, &linkaddr_node_addr)) {
      unicast_send(&uc, &addr);
      printf("sent!");
    }
  }
  
  while(1){
    
    if (state == 2){
      // Countdown
      printf("Countdown %d\n", counter); 
      PORTF |= (1 << PF2) | (1 << PF3);
      etimer_set(&et, CLOCK_SECOND/2);
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
      PORTF &= ~(1 << PF2);
      PORTF &= ~(1 << PF3);
      etimer_set(&et, CLOCK_SECOND/2);
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
      if (counter == 3){
	state = 3;
	counter = 0;
	EICRA |= ((1 << ISC01) | (1 << ISC11));   // Enable external interrupts
	EIMSK |= ((1 << INT0) | (1 << INT1));
      }
      counter++;
    }

    // IDEA: Implementar l'state == 4, que encen i apaga els LEDs del winner fins que es torna a començar
    else{
      etimer_set(&et, CLOCK_SECOND/2);
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
      //PORTF &= ~(1 << PF2);
      //PORTF &= ~(1 << PF3);
    } 
  }
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/

ISR(INT0_vect){
  packetbuf_copyfrom("CAR 1", 6);
  unicast_send(&uc, &addr);
  printf("CAR 1, state = %d \n", state);
}

ISR(INT1_vect){
  packetbuf_copyfrom("CAR 2", 6);
  unicast_send(&uc, &addr);
  printf("CAR 2, state = %d \n", state);
}
