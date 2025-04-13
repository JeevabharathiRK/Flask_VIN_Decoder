from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def vinIND(vin):
    # 🔧 Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://rtovehicle.info/vindecoder")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "«Rj3qrlb»-form-item"))
        )

        vin_input = driver.find_element(By.ID, "«Rj3qrlb»-form-item")
        vin_input.send_keys(vin)
        vin_input.send_keys(Keys.RETURN)

        result_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rounded-2xl border')]"))
        )

        raw_text = result_div.text.strip().splitlines()
        data = {}

        # Parse every pair of lines
        for i in range(len(raw_text) - 1):
            key_candidate = raw_text[i].strip().upper()
            val_candidate = raw_text[i + 1].strip()

            # You can add more expected keys here as needed
            expected_keys = [
                "CATEGORY", "SERIAL", "MAKE", "MODEL",
                "MANUFACTURE MONTH", "MANUFACTURE YEAR"
            ]

            if key_candidate in expected_keys:
                data[key_candidate.title()] = val_candidate

        print("\n✅ Parsed Dictionary:\n", data)
        return data

    except Exception as e:
        print("❌ Error occurred:", e)
        return {"error": str(e)}
    finally:
        driver.quit()
