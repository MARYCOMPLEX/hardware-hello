#include <inttypes.h>
#include "sdkconfig.h"
#include "esp_err.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

void app_main(void) {
    uint32_t count = 0;
#if CONFIG_HH_ENABLE_LED
    // Valid silicon GPIO still requires board-level wiring verification.
    ESP_ERROR_CHECK(GPIO_IS_VALID_OUTPUT_GPIO(CONFIG_HH_LED_GPIO)
                    ? ESP_OK : ESP_ERR_INVALID_ARG);
    gpio_config_t cfg = {
        .pin_bit_mask = 1ULL << CONFIG_HH_LED_GPIO,
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&cfg));
#endif
    while (1) {
        ESP_LOGI("hello", "tick=%" PRIu32, count);
#if CONFIG_HH_ENABLE_LED
        ESP_ERROR_CHECK(gpio_set_level(CONFIG_HH_LED_GPIO, count & 1U));
#endif
        ++count;
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
