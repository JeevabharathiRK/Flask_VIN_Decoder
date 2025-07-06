from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def vinIND(vin):
    # 🔧 Setup Chrome in headless mode (set to True if you don't want GUI)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ❌ Remove this line if you want to see the browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    # Start the browser
    driver = webdriver.Chrome(options=options)

    try:
        print("🌐 Loading VIN decoder site...")
        driver.get("https://rtovehicle.info/vindecoder")

        # ✅ Wait and locate the input field using `name` (safe)
        vin_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='vin_number']"))
        )

        print(f"✍️ Typing VIN: {vin}")
        vin_input.send_keys(vin)
        vin_input.send_keys(Keys.RETURN)

        # ✅ Wait for the results section to appear
        result_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rounded-2xl border')]"))
        )

        raw_text = result_div.text.strip().splitlines()
        data = {}

        expected_keys = [
            "CATEGORY", "SERIAL", "MAKE", "MODEL",
            "MANUFACTURE MONTH", "MANUFACTURE YEAR"
        ]

        for i in range(len(raw_text) - 1):
            key_candidate = raw_text[i].strip().upper()
            val_candidate = raw_text[i + 1].strip()
            if key_candidate in expected_keys:
                data[key_candidate.title()] = val_candidate

        print("\n✅ Vehicle Details Extracted:\n")
        for k, v in data.items():
            print(f"{k}: {v}")

        return data

    except Exception as e:
        print("\n❌ Error occurred:", e)
        return {"error": str(e)}

    finally:
        driver.quit()