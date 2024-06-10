/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * main.c
 * Copyright (C) 2020 coap_server Vladimir Roncevic <elektron.ronca@gmail.com>
 *
 * coap_server is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * coap_server is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "server_api.h"

int main(int argc, char* argv[]) {
    coap_context_t* ctx;
    coap_address_t serv_addr;
    coap_resource_t* time_resource;
    fd_set readfds;

    /* Prepare the CoAP server socket */
    coap_address_init(&serv_addr);
    serv_addr.addr.sin.sin_family = AF_INET;
    serv_addr.addr.sin.sin_addr.s_addr = INADDR_ANY;
    serv_addr.addr.sin.sin_port = htons(5683);
    ctx = coap_new_context(&serv_addr);
    if (!ctx) {
        exit(EXIT_FAILURE);
    }

    /* Initialize the hello resource */
    time_resource = coap_resource_init((unsigned char *)"time", 4, 0);
    coap_register_handler(time_resource, COAP_REQUEST_GET, time_handler);
    coap_add_resource(ctx, time_resource);

    /* Listen for incoming connections */
    while (1) {
        FD_ZERO(&readfds);
        FD_SET(ctx->sockfd, &readfds);
        int result = select(FD_SETSIZE, &readfds, 0, 0, NULL);
        if (result < 0) {
            exit(EXIT_FAILURE);
        } else if (result > 0 && FD_ISSET(ctx->sockfd, &readfds)) {
            coap_read(ctx);
        }
    }
}

