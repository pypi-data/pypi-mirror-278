/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * time_handler.c
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

void time_handler(
    coap_context_t *ctx, struct coap_resource_t *resource,
    const coap_endpoint_t *local_interface, coap_address_t *peer,
    coap_pdu_t *request, str *token, coap_pdu_t *response
) {
    unsigned char buffer_data[3];
    const char* response_data = get_time();
    response->hdr->code = COAP_RESPONSE_CODE(205);
    coap_add_option(
        response, COAP_OPTION_CONTENT_TYPE,
        coap_encode_var_bytes(buffer_data, COAP_MEDIATYPE_TEXT_PLAIN),
        buffer_data
    );
    coap_add_data(
        response, strlen(response_data), (unsigned char *)response_data
    );
}

