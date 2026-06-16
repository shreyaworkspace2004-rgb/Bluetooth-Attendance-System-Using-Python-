import asyncio
from bleak import BleakScanner
import pandas as pd
from datetime import datetime

# 👉 Step 1: Give your divece MAC adress here
students = {
    "79:E8:7E:28:C7:3D": "Shreya"   # Your device
}

file_name = "attendance.csv"

# 👉 CSV file create (if not exists)
try:
    df = pd.read_csv(file_name)
except:
    df = pd.DataFrame(columns=["Name", "MAC", "Time"])
    df.to_csv(file_name, index=False)

# 👉 Main function
async def attendance_system():
    print("📡 Scanning for devices...\n")

    marked = set()

    while True:
        devices = await BleakScanner.discover(timeout=8)

        if not devices:
            print("❌ No devices found\n")

        for device in devices:
            mac = device.address.upper()
            name = device.name

            # 👉 Debug print (Shows all devices)
            print(f"Detected: {mac} | {name}")

            # 👉 Match check
            if mac in students and mac not in marked:
                student_name = students[mac]
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print(f"\n✅ Attendance Marked: {student_name}\n")

                # 👉 Save to CSV
                new_data = pd.DataFrame([[student_name, mac, time_now]],
                                        columns=["Name", "MAC", "Time"])
                new_data.to_csv(file_name, mode='a', header=False, index=False)

                marked.add(mac)

        print("\n🔄 Scanning again...\n")
        await asyncio.sleep(5)

# 👉 Run
asyncio.run(attendance_system())