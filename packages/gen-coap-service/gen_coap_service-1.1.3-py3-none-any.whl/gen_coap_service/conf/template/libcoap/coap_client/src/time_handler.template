/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * time_handler.c
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

/**
 * Description:
 *     Getting current local time on host.
 *
 * Arguments:
 *     None
 *
 * Return value:
 *     Current local time from host in string format | NULL.
 */
void time_handler(
    struct coap_context_t *ctx, const coap_endpoint_t *local_interface,
    const coap_address_t *remote, coap_pdu_t *sent, coap_pdu_t *received,
    const coap_tid_t id
) {
    unsigned char* data;
    size_t data_len;
    if (COAP_RESPONSE_CLASS(received->hdr->code) == 2) {
        if (coap_get_data(received, &data_len, &data)) {
            printf("Received: %s\n", data);
        }
    }
}

