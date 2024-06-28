#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/uart.h"
#include "driver/gpio.h"

#define BUF_SIZE    1024
#define TX_PIN      1
#define RX_PIN      3
#define CHARGE      18
#define DCL_EIS     19
#define EIS_RESET_1 22
#define EIS_RESET_2 23
#define TC_ALARM    33
#define DCL_ALARM   32

static QueueHandle_t uart0_queue;

static void uart_event_task(void *pvParameters) {
    uart_event_t event;
    uint8_t* dtmp = (uint8_t*) malloc(BUF_SIZE);
    uint8_t* buffer = (uint8_t*) calloc(1, BUF_SIZE);
    int buffer_len = 0;

    for(;;) {
        // Espera por dados da UART
        if(xQueueReceive(uart0_queue, (void * )&event, portMAX_DELAY)) {
            bzero(dtmp, BUF_SIZE);
            switch(event.type) {
                case UART_DATA:
                    uart_read_bytes(UART_NUM_0, dtmp, event.size, portMAX_DELAY);
                    for (int i = 0; i < event.size; ++i) {
                        buffer[buffer_len++] = dtmp[i];
                        if (dtmp[i] == ',') {
                            char *token = strtok((char *)buffer, ",");
                            if (strcmp(token, "CHARGE ON") == 0) {
                                gpio_set_level(CHARGE, 1);
                            } else if (strcmp(token, "CHARGE OFF") == 0) {
                                gpio_set_level(CHARGE, 0);
                            } else if (strcmp(token, "DCL_EIS ON") == 0) {
                                gpio_set_level(DCL_EIS, 1);
                            } else if (strcmp(token, "DCL_EIS OFF") == 0) {
                                gpio_set_level(DCL_EIS, 0);
                            } else if (strcmp(token, "RESET_EIS1") == 0) {
                                gpio_set_level(EIS_RESET_1, 1);
                                vTaskDelay(500 / portTICK_PERIOD_MS);
                                gpio_set_level(EIS_RESET_1, 0);
                            } else if (strcmp(token, "RESET_EIS2") == 0) {
                                gpio_set_level(EIS_RESET_2, 1);
                                vTaskDelay(500 / portTICK_PERIOD_MS);
                                gpio_set_level(EIS_RESET_2, 0);
                            } else if (strcmp(token, "TC_ALARM?") == 0) {
                                char msg[50];
                                sprintf(msg, "TC_ALARM %s\n",
                                    gpio_get_level(TC_ALARM) ? "ON" : "OFF");
                                uart_write_bytes(UART_NUM_0, msg, strlen(msg));
                            } else if (strcmp(token, "DCL_ALARM?") == 0) {
                                char msg[50];
                                sprintf(msg, "DCL_ALARM %s\n",
                                    gpio_get_level(DCL_ALARM) ? "ON" : "OFF");
                                uart_write_bytes(UART_NUM_0, msg, strlen(msg));
                            }
                            buffer_len = 0;
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    }
    free(dtmp);
    free(buffer);
    vTaskDelete(NULL);
}

void app_main() {
    uart_config_t uart_config = {
        .baud_rate = 9600,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    uart_param_config(UART_NUM_0, &uart_config);
    uart_set_pin(UART_NUM_0, TX_PIN, RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM_0, BUF_SIZE * 2, 0, 20, &uart0_queue, 0);

    gpio_set_direction(CHARGE, GPIO_MODE_OUTPUT);
    gpio_set_direction(DCL_EIS, GPIO_MODE_OUTPUT);
    gpio_set_direction(EIS_RESET_1, GPIO_MODE_OUTPUT);
    gpio_set_direction(EIS_RESET_2, GPIO_MODE_OUTPUT);
    gpio_set_direction(TC_ALARM, GPIO_MODE_INPUT);
    gpio_set_direction(DCL_ALARM, GPIO_MODE_INPUT);

    xTaskCreate(uart_event_task, "uart_event_task", 2048, NULL, 12, NULL);
}
