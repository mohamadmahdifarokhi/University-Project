import math
from tabulate import tabulate

class Device:
    def __init__(self, name, power_required, frequency, ac_voltage=220):
        self.resistance = None
        self.name = name
        self.power_required = power_required
        self.frequency = frequency
        self.ac_voltage = ac_voltage
        self.ac_current = None
        self.dc_current = None  # Initialize dc_current attribute

    def to_dict(self):
        return {
            'name': self.name,
            'ac_voltage': self.ac_voltage,
            'ac_current': self.ac_current,
            'frequency': self.frequency
        }
    def from_dict(cls, data):
        return cls

    def convert_ac_to_dc(self):
        # Constants for a basic rectifier model
        peak_factor = math.sqrt(2)  # Assuming a sine wave AC input
        rectification_factor = 0.9  # Efficiency of rectification process
        # Calculate peak AC voltage
        peak_ac_voltage = self.ac_voltage * peak_factor
        # Calculate pulsating DC voltage
        pulsating_dc_voltage = peak_ac_voltage * rectification_factor
        # Calculate average DC voltage
        average_dc_voltage = pulsating_dc_voltage / math.sqrt(2)
        # Calculate efficiency
        efficiency = (average_dc_voltage / peak_ac_voltage) * 100
        return average_dc_voltage, efficiency

    def calculate_ac_current(self):
        # Calculate AC current using P = VI (for AC)
        self.ac_current = self.power_required / self.ac_voltage
        return self.ac_current

    def calculate_power(self):
        # Calculate power using P = VI (for DC)
        dc_voltage, _ = self.convert_ac_to_dc()  # Extract average DC voltage from the tuple
        power = dc_voltage * self.ac_current
        return power

    def calculate_power_ac(self):
        # Calculate power using P = VI (for AC)
        power = self.ac_voltage * self.ac_current
        return power

    def calculate_load_resistance(self):
        # Using Ohm's Law to calculate AC current for a resistive load
        resistance = self.ac_voltage / self.ac_current
        return resistance

    def calculate_working_hours(self, energy_consumed):
        # Calculate working hours using the formula: time = energy / power
        power = self.calculate_power()
        working_hours = energy_consumed / power
        return working_hours

    def calculate_dc_current(self):
        # Perform AC to DC conversion
        dc_voltage, _ = self.convert_ac_to_dc()  # Extract average DC voltage from the tuple
        # Using Ohm's Law to calculate DC current
        self.dc_current = dc_voltage / self.resistance  # Update dc_current attribute
        return self.dc_current  # Return the calculated DC current

class SolarPanel:
    def __init__(self, efficiency):
        self.efficiency = efficiency  # Efficiency of the solar panel

    def generate_power(self, power_required, generating_hours):
        # Assuming solar power generation is proportional to required power and generating hours
        generated_power = (power_required / self.efficiency) * generating_hours
        return generated_power

class Battery:
    def __init__(self, capacity):
        self.capacity = capacity  # Capacity of the battery
        self.charge = 0  # Initial charge level

    def charge_battery(self, power):
        # Charge the battery with the provided power
        self.charge += power
        # Ensure the charge does not exceed the battery capacity
        self.charge = min(self.charge, self.capacity)

class Conversion:
    @staticmethod
    def percent(delta_L, L_ori, delta_S, S_de):
        CPL = delta_L / L_ori
        CPS = delta_S / S_de
        return CPL, CPS

class Energy:
    @staticmethod
    def saved_energy(L_ori_t, delta_eta_t):
        SE = sum(L_ori_t * delta_eta_t for L_ori_t, delta_eta_t in zip(L_ori_t, delta_eta_t))
        return SE

    @staticmethod
    def investment_and_saving(cost_eq, p, SE, S_re, x):
        INV = sum(cost_eq)
        SAV = p * SE * x + p * S_re * x
        return INV, SAV

class Emissions:
    @staticmethod
    def greenhouse_emission_saving(EMA_f, EMB_e):
        return EMA_f, EMB_e

class Efficiency:
    @staticmethod
    def calculate_efficiency(L_ori, S_up, S_pv, EFF_ori, delta_eta):
        EFF = L_ori / (S_up + S_pv)
        S_up_calculated = (L_ori - S_pv) / (EFF_ori + delta_eta)
        return EFF, S_up_calculated

def calculate_cooling_load_ac(square_feet):
    cooling_load_per_sqft = 20  # Adjust this based on your specific needs
    cooling_load_ac = square_feet * cooling_load_per_sqft
    return cooling_load_ac

def square_feet_to_square_meters(square_feet):
    square_meters = square_feet / 10.7639
    return square_meters

def calculate_fixed_load_ac(ac_capacity):
    fixed_load_factor = 0.2  # Adjust this based on your specific needs
    fixed_load_ac = ac_capacity * fixed_load_factor
    return fixed_load_ac

def calculate_fixed_load_dc(dc_ac_capacity):
    fixed_load_factor = 0.15  # Adjust this based on your specific needs
    fixed_load_dc = dc_ac_capacity * fixed_load_factor
    return fixed_load_dc

def calculate_ac_current_voltage(ac_capacity, ac_resistance, ac_impedance):
    ac_voltage_current = ac_capacity / ac_impedance
    return ac_voltage_current

def calculate_dc_current_voltage(dc_ac_capacity, dc_resistance, dc_impedance):
    dc_voltage_current = dc_ac_capacity / dc_impedance
    return dc_voltage_current

def calculate_cooling_load_dc(square_feet):
    cooling_load_per_sqft = 20  # Adjust this based on your specific needs
    cooling_load_dc = square_feet * cooling_load_per_sqft
    return cooling_load_dc

def calculate_ac_capacity(cooling_load):
    efficiency_factor = 1.5  # Adjust this based on your specific needs
    ac_capacity_watts = cooling_load * efficiency_factor
    return ac_capacity_watts

def calculate_dc_ac_capacity(cooling_load):
    dc_efficiency_factor = 1.2  # Adjust this based on your specific needs
    dc_ac_capacity_watts = cooling_load * dc_efficiency_factor
    return dc_ac_capacity_watts

def calculate_annual_cost_ac(ac_capacity_kwh, cost_per_kwh, hours_per_day=8, days_per_year=365):
    annual_energy_consumption_ac = ac_capacity_kwh * hours_per_day * days_per_year
    annual_cost_ac = annual_energy_consumption_ac * cost_per_kwh
    return annual_cost_ac

def calculate_annual_cost_dc(dc_ac_capacity_kwh, cost_per_kwh, hours_per_day=8, days_per_year=365):
    annual_energy_consumption_dc = dc_ac_capacity_kwh * hours_per_day * days_per_year
    annual_cost_dc = annual_energy_consumption_dc * cost_per_kwh
    return annual_cost_dc

def calculate_resistance_ac(ac_capacity):
    power_factor = 0.8  # Assume a typical power factor
    COP = 1.5  # Assume a typical COP for air conditioners
    watts_to_btu = 3412  # Conversion factor from watts to BTU/h
    resistance = ac_capacity / (power_factor * COP * watts_to_btu)
    return resistance

def calculate_voltage_ac(ac_capacity, resistance, inductive_reactance):
    impedance = resistance + 1j * inductive_reactance
    current_ac = ac_capacity / impedance
    voltage_ac = current_ac * impedance
    return voltage_ac

def calculate_ac_resistance(ac_capacity):
    power_factor = 0.8  # Assume a typical power factor
    COP = 1.5  # Assume a typical COP for air conditioners
    watts_to_btu = 3412  # Conversion factor from watts to BTU/h
    resistance = ac_capacity / (power_factor * COP * watts_to_btu)
    return resistance

def calculate_reactance(operating_voltage, current, ac_capacity_watts=None):
    impedance = operating_voltage / current
    resistance = calculate_resistance_ac(ac_capacity_watts)
    inductive_reactance = impedance - resistance
    return inductive_reactance

def calculate_dc_resistance(dc_ac_capacity):
    power_factor = 0.8  # Assume a typical power factor
    dc_resistance_factor = 1.2  # Adjust this based on your specific needs
    resistance = dc_ac_capacity / (power_factor * dc_resistance_factor)
    return resistance

def calculate_ac_impedance(ac_capacity):
    power_factor = 0.8  # Assume a typical power factor
    COP = 1.5  # Assume a typical COP for air conditioners
    watts_to_btu = 3412  # Conversion factor from watts to BTU/h
    resistance = ac_capacity / (power_factor * COP * watts_to_btu)
    inductive_reactance = 220 / 10  # Assuming a typical operating voltage of 220VAC and a current of 10A
    impedance = resistance + 1j * inductive_reactance
    return impedance

def calculate_dc_impedance(dc_ac_capacity):
    power_factor = 0.8  # Assume a typical power factor
    dc_resistance_factor = 1.2  # Adjust this based on your specific needs
    dc_voltage = 220  # Assuming a typical operating voltage of 220VDC
    dc_current = dc_ac_capacity / dc_voltage
    dc_impedance = dc_voltage / dc_current
    return dc_impedance

def main():
    global device, device_name, working_hours, emissions_savings
    ac_voltage = 220  # Fixed AC voltage as 220V
    frequency = 50  # Fixed frequency as 50Hz

    cost_dc = 0.079  # Cost of power in DC (euro/KWh)
    cost_ac = 0.148  # Cost of power in AC (euro/KWh)

    square_meters = float(input("Enter the square meters of the area to be cooled: "))
    desired_temperature = float(input("Enter the desired temperature to be maintained (in Celsius): "))

    num_appliances = int(input("Enter the number of other appliances: ")) + 1  # Including the AC

    appliances = []

    total_power_dc = 0
    total_power_ac = 0
    total_energy_consumed_ac = 0
    total_energy_consumed_dc = 0
    total_cost_dc = 0
    total_cost_ac = 0
    total_ac_power_consumed = 0

    for i in range(num_appliances):
        if i == 0:
            device_name = "Air Conditioner"
            power_required = 0  # Power for AC will be calculated based on cooling load
            working_hours = 24

            cooling_load_ac = calculate_cooling_load_ac(square_meters)
            cooling_load_dc = calculate_cooling_load_dc(square_meters)

            ac_capacity_watts = calculate_ac_capacity(cooling_load_ac)
            ac_capacity_kwh = ac_capacity_watts / 1000
            dc_ac_capacity_watts = calculate_dc_ac_capacity(cooling_load_dc)
            fixed_load_ac = calculate_fixed_load_ac(ac_capacity_watts)
            fixed_load_dc = calculate_fixed_load_dc(dc_ac_capacity_watts)

            device = Device(device_name, ac_capacity_watts, frequency)
        else:
            print(f"\n--- Appliance {i} ---")
            device_name = input("Enter device Name: ")
            power_required = float(input("Enter power required to run the appliance (in watts): "))
            working_hours = float(input(f"Enter working time of the {device_name} in hours: "))

            device = Device(device_name, power_required, frequency)

        ac_current = device.calculate_ac_current()
        power_dc = device.calculate_power()
        power_ac = device.calculate_power_ac()

        energy_consumed_ac = power_ac * (working_hours / 1000)
        energy_consumed_dc = power_dc * (working_hours / 1000)

        appliances.append((device, working_hours))

        total_power_dc += power_dc
        total_power_ac += power_ac
        total_energy_consumed_ac += energy_consumed_ac
        total_energy_consumed_dc += energy_consumed_dc
        total_cost_dc += (power_dc * working_hours * (cost_dc / 1000))  # Convert cost to kWh
        total_cost_ac += (power_ac * working_hours * (cost_ac / 1000))  # Convert cost to kWh

        device.resistance = device.calculate_load_resistance()
        ac_power_consumed = power_ac * (working_hours / 1000)  # Convert watt-hours to kilowatt-hours
        total_ac_power_consumed += ac_power_consumed

    generating_hours = float(input("Enter solar power generating hours: "))

    if square_meters < 50:
        solar_panel_capacity_kw = 1
    elif square_meters <= 75:
        solar_panel_capacity_kw = 2
    elif square_meters <= 100:
        solar_panel_capacity_kw = 3
    elif square_meters <= 125:
        solar_panel_capacity_kw = 4
    elif square_meters <= 150:
        solar_panel_capacity_kw = 5
    elif square_meters <= 175:
        solar_panel_capacity_kw = 6
    elif square_meters <= 200:
        solar_panel_capacity_kw = 7
    elif square_meters <= 225:
        solar_panel_capacity_kw = 8
    else:
        solar_panel_capacity_kw = 9

    solar_panel = SolarPanel(efficiency=0.15)
    generated_power_dc = solar_panel_capacity_kw * generating_hours

    print("\n--- Total Summary ---")
    print(f"Total power consumed (DC): {total_power_dc:.2f} Watts")
    print(f"Total power consumed (AC): {total_power_ac:.2f} Watts")
    print(f"Total energy consumed (AC): {total_energy_consumed_ac:.2f} kWh")
    print(f"Total energy consumed (DC): {total_energy_consumed_dc:.2f} kWh")
    print(f"Total cost for power consumed (DC): {total_cost_dc:.2f} €")
    print(f"Total cost for power consumed (AC): {total_cost_ac:.2f} €")
    print(f"Power generated from solar power (DC): {generated_power_dc:.2f} kWh")

    excess_power = 0
    battery = None

    if solar_panel_capacity_kw <= 1:
        battery_capacity = 4  # kWh
    elif solar_panel_capacity_kw <= 2:
        battery_capacity = 8  # kWh
    elif solar_panel_capacity_kw <= 3:
        battery_capacity = 12  # kWh
    elif solar_panel_capacity_kw <= 4:
        battery_capacity = 16  # kWh
    elif solar_panel_capacity_kw <= 5:
        battery_capacity = 20  # kWh
    elif solar_panel_capacity_kw <= 6:
        battery_capacity = 24  # kWh
    elif solar_panel_capacity_kw <= 7:
        battery_capacity = 28  # kWh
    elif solar_panel_capacity_kw <= 8:
        battery_capacity = 32  # kWh
    else:
        battery_capacity = 36  # kWh

    excess_power = generated_power_dc - battery_capacity

    if excess_power > 0:
        battery = Battery(battery_capacity)
        battery.charge_battery(generated_power_dc)
        print(f"Battery capacity: {battery.capacity:.2f} kWh")
        print(f"Battery charge level: {battery.charge:.2f} kWh")
        if excess_power > 0:
            print(f"Excess power (DC): {excess_power:.2f} kWh")
    else:
        print("No excess power generated.")

    for appliance, working_hours in appliances:
        appliance_power_utilization = (appliance.calculate_power_ac() * working_hours / 1000) / total_power_dc * 100
        print(f"Appliance power utilization for {appliance.name}: {appliance_power_utilization:.2f}%")

    headers_individual = ["Device Name", "AC Voltage (V)", "AC Frequency (Hz)", "DC Voltage (estimated) (V)",
                          "Load Resistance (ohms)", "DC Current (estimated) (A)", "Power (DC estimated) (W)",
                          "Energy Consumed (AC estimated) (kWh)", "Energy Consumed (DC estimated) (kWh)"]
    data_individual = []

    for appliance, _ in appliances:
        data_individual.append([appliance.name,
                                appliance.ac_voltage,
                                appliance.frequency,
                                appliance.convert_ac_to_dc()[0],
                                appliance.resistance,
                                appliance.calculate_dc_current(),
                                appliance.calculate_power(),
                                appliance.calculate_power_ac() * (working_hours / 1000),
                                total_energy_consumed_dc])

    print(tabulate(data_individual, headers=headers_individual, tablefmt="grid"))

    battery_usage_percentage = (battery.charge / generated_power_dc) * 100 if generated_power_dc > 0 else 0
    print(f"Battery usage efficiency: {battery_usage_percentage:.2f}%")

    average_emissions_intensity_ac = 475  # gCO2/kWh
    improvement_percentage = 10  # 10% improvement
    average_emissions_intensity = 50  # gCO2/kwh

    improved_emissions_intensity_ac = average_emissions_intensity_ac * (1 - improvement_percentage / 100)
    improved_emissions_intensity = average_emissions_intensity * (1 - improvement_percentage / 100)
    original_emissions_intensity_ac = average_emissions_intensity_ac
    original_emissions_intensity = average_emissions_intensity

    emissions_intensity_difference_ac = original_emissions_intensity_ac - improved_emissions_intensity_ac
    emissions_intensity_difference = original_emissions_intensity - improved_emissions_intensity

    constant_power_sector_emissions = (emissions_intensity_difference_ac * total_power_ac / 1000)  # Convert grams to kg
    power_sector_emissions = (emissions_intensity_difference * (total_power_dc / 1000))

    print(f"Power Sector Emissions for your consumption in AC: {constant_power_sector_emissions:.2f} metric tonnes of CO2")
    emissions_savings_ac = constant_power_sector_emissions
    trees_planted_equivalent_ac = (emissions_savings_ac / 22) * 1000
    print(f"Equivalent trees to purify the Green house gas emissions: {trees_planted_equivalent_ac:.2f}")

    emissions_savings = power_sector_emissions
    print(f"Power Sector Emissions for your consumption Green house gas emissions in Solar Power: {power_sector_emissions:.2f} metric tonnes of CO2")
    trees_planted_equivalent = (emissions_savings / 22) * 1000
    print(f"Equivalent trees to purify the Green house gas emissions savings: {trees_planted_equivalent:.2f}")

    # Integration of additional calculations

    # Conversion Percent Calculation
    CPL, CPS = Conversion.percent(delta_L=500, L_ori=1000, delta_S=600, S_de=1200)
    print(f"CPL: {CPL}, CPS: {CPS}")

    # Saved Energy Calculation
    SE = Energy.saved_energy(L_ori_t=[100, 150, 120, 130, 110, 160, 140, 150, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280], delta_eta_t=[0.1] * 24)
    print(f"Saved Energy: {SE}")

    # Investment and Saving Calculation
    INV, SAV = Energy.investment_and_saving(cost_eq=[1000, 2000, 1500], p=0.15, SE=1000, S_re=500, x=30)
    print(f"Investment: {INV}, Saving: {SAV}")

    # Greenhouse Emission Saving Calculation
    EMA_f, EMB_e = Emissions.greenhouse_emission_saving(EMA_f=100, EMB_e=80)
    print(f"Greenhouse Emission Saving - EMA_f: {EMA_f}, EMB_e: {EMB_e}")

    # Efficiency Calculation
    EFF, S_up_calculated = Efficiency.calculate_efficiency(L_ori=1000, S_up=400, S_pv=600, EFF_ori=0.85, delta_eta=0.1)
    print(f"Efficiency: {EFF}, S_up_calculated: {S_up_calculated}")

if __name__ == "__main__":
    main()
