/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * main.c
 * Copyright (C) 2020 coap_client Vladimir Roncevic <elektron.ronca@gmail.com>
 *
 * coap_client is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * coap_client is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "client_api.h"

int verbose = 0;

/**
 * Description:
 *     Main entry point.
 *
 * Arguments:
 *     args - Number of arguments.
*      argv - Array of arguments.
 *
 * Return value:
 *     Success (0) | Exit return code.
 */
int main(int argc, char* argv[]) {

    int option;
    coap_context_t* ctx;
    coap_address_t dst_addr, src_addr;
    static coap_uri_t uri;
    fd_set readfds;
    coap_pdu_t* request;

    option = process_options(argc, argv);

    print_verbose(verbose, "Prepare coap socket start\n");
    coap_address_init(&src_addr);
    src_addr.addr.sin.sin_family = AF_INET;
    src_addr.addr.sin.sin_port = htons(CLIENT_PORT);
    src_addr.addr.sin.sin_addr.s_addr = inet_addr(CLIENT_IP);
    ctx = coap_new_context(&src_addr);
    print_verbose(verbose, "Prepare coap socket end\n");

    coap_address_init(&dst_addr);
    dst_addr.addr.sin.sin_family = AF_INET;
    dst_addr.addr.sin.sin_port = htons(SERVER_PORT);
    dst_addr.addr.sin.sin_addr.s_addr = inet_addr(SERVER_IP);

    print_verbose(verbose, "Prepare the request start\n");
    coap_split_uri(SERVER_URI, strlen(SERVER_URI), &uri);
    request = coap_new_pdu();
    request->hdr->type = COAP_MESSAGE_CON;
    request->hdr->id = coap_new_message_id(ctx);
    request->hdr->code = GET_METHOD;
    coap_add_option(
        request, COAP_OPTION_URI_PATH, uri.path.length, uri.path.s
    );
    print_verbose(verbose, "Prepare the request end\n");

    print_verbose(verbose, "Prepare and set the handler start\n");
    coap_register_response_handler(ctx, time_handler);
    print_verbose(verbose, "Prepare and set the handler end\n");
    print_verbose(verbose, "Prepare and send the request start\n");
    coap_send_confirmed(ctx, ctx->endpoint, &dst_addr, request);
    FD_ZERO(&readfds);
    FD_SET(ctx->sockfd, &readfds);
    print_verbose(verbose, "Prepare and send the request end\n");
    int result = select(FD_SETSIZE, &readfds, 0, 0, NULL);
    if (result < 0) {
        exit(EXIT_FAILURE);
    } else if (result > 0 && FD_ISSET(ctx->sockfd, &readfds)) {
        coap_read(ctx);
    }
    return 0;
}

