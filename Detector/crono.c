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
#include "lib/list.h"
#include "lib/memb.h"

#include "dev/button-sensor.h"

#include "dev/leds.h"

#include <stdio.h>
#include <string.h>
#include <avr/interrupt.h>

/*---------------------------------------------------------------------------*/
PROCESS(unicast_process, "Unicast process");
PROCESS(broadcast_process, "Broadcast process");
AUTOSTART_PROCESSES(&unicast_process, &broadcast_process);
/*---------------------------------------------------------------------------*/
// IDEA afegir de qui es reben els missatges al transmetreho pel serial per tal d'identificar els splits
// IDEA el pin check remotes es pot connectar al RESET
static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from){
  printf("ddd");}

static void
unicast_recv(struct unicast_conn *c, const linkaddr_t *from)
{
  // Prints the received packets
  printf("%s\n", (char *)packetbuf_dataptr());
}

static const struct broadcast_callbacks broadcast_callbacks = {broadcast_recv};
static struct broadcast_conn bc;

static const struct unicast_callbacks unicast_callbacks = {unicast_recv};
static struct unicast_conn uc;

PROCESS_THREAD(broadcast_process, ev, data){
  static struct etimer et;
  
  PROCESS_EXITHANDLER(broadcast_close(&bc);)
  PROCESS_BEGIN();
  
  broadcast_open(&bc, 129, &broadcast_callbacks);
  etimer_set(&et, CLOCK_SECOND * 8);  
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
  packetbuf_copyfrom("READY", 6);
  broadcast_send(&bc);
  printf("broadcast sent\n");
  
  while(1) {
    etimer_set(&et, CLOCK_SECOND * 8);  
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
  }
  
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(unicast_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&uc);)
    
  PROCESS_BEGIN();
  DDRD &= ~(1 << DDD0);
  DDRD &= ~(1 << DDD1);
  PORTD |= ((1 << PD0) | (1 << PD1)); // External interrupts 
  
  DDRE &= ~(1 << DDE6);
  //DDRE &= ~(1 << DDE7);

  //PORTE |= ((1 << PE6) | (1 << PE7));
  PORTE |= (1 << PE6);
  
  sei();
  EICRA |= ((1 << ISC01) | (1 << ISC11));
  //EICRB |= ((1 << ISC61) | (1 << ISC71));
  EICRB |= (1 << ISC61);
  EIMSK |= ((1 << INT0) | (1 << INT1) | (1 << INT6)); // | (1 << INT7));
  
  unicast_open(&uc, 146, &unicast_callbacks);
  static struct etimer et;
  
  while(1) {
    
    etimer_set(&et, CLOCK_SECOND);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
    
  }
  PROCESS_END();
}
/*---------------------------------------------------------------------------*/



ISR(INT0_vect){
  packetbuf_copyfrom("WIN 1", 6);
  broadcast_send(&bc);
  printf("WIN 1 sent\n");
}

ISR(INT1_vect){
  packetbuf_copyfrom("WIN 2", 6);
  broadcast_send(&bc);
  printf("WIN 2 sent\n");
}

ISR(INT6_vect){
  packetbuf_copyfrom("START", 6);
  broadcast_send(&bc);
  printf("START sent\n");
}

/*ISR(INT7_vect){
  packetbuf_copyfrom("LAP", 4);
  broadcast_send(&bc);
  printf("LAP sent\n");
  }*/
