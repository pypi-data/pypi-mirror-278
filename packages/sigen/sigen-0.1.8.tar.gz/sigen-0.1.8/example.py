import logging
import os
import asyncio
from sigen import Sigen

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    # Read username and password from environment variables
    username = os.getenv('SIGEN_USERNAME')
    password = os.getenv('SIGEN_PASSWORD')

    if not username or not password:
        logging.error("Environment variables SIGEN_USERNAME and SIGEN_PASSWORD must be set")
        return

    # username and password you use in the mySigen app.
    # Region is Europe (eu) / Asia-Pacific (apac) /
    # Middle East & Africa (eu) / Chinese Mainland (cn) / Unitest States (us)
    sigen = Sigen(username=username, password=password, region="eu")

    # Initialize the Sigen instance
    await sigen.async_initialize()

    # Fetch and log station info
    logger.info("Fetching station info...")
    station_info = await sigen.fetch_station_info()
    logger.info("Station Info:")
    logger.info(f"Station ID: {station_info['stationId']}")
    logger.info(f"Has PV: {station_info['hasPv']}")
    logger.info(f"Has EV: {station_info['hasEv']}")
    logger.info(f"On Grid: {station_info['onGrid']}")
    logger.info(f"PV Capacity: {station_info['pvCapacity']} kW")
    logger.info(f"Battery Capacity: {station_info['batteryCapacity']} kWh")

    # Fetch and log energy flow info
    logger.info("\nFetching energy flow info...")
    energy_flow = await sigen.get_energy_flow()
    logger.info("Energy Flow Info:")
    logger.info(f"PV Day Energy: {energy_flow['pvDayNrg']} kWh")
    logger.info(f"PV Power: {energy_flow['pvPower']} kW")
    logger.info(f"Buy/Sell Power: {energy_flow['buySellPower']} kW")
    logger.info(f"EV Power: {energy_flow['evPower']} kW")
    logger.info(f"AC Power: {energy_flow['acPower']} kW")
    logger.info(f"Load Power: {energy_flow['loadPower']} kW")
    logger.info(f"Battery Power: {energy_flow['batteryPower']} kW")
    logger.info(f"Battery SOC: {energy_flow['batterySoc']}%")

    # Fetch and log current operational mode
    logger.info("\nFetching current operational mode...")
    current_mode = await sigen.get_operational_mode()
    logger.info(f"Current Operational Mode: {current_mode}")

    # Change operational mode (example: setting mode to 'Fully Fed to Grid')
    # logger.info("\nSetting operational mode to 'Fully Fed to Grid'...")
    # response = await sigen.set_operational_mode(5)

    # Or set by label
    # response = await sigen.set_operational_mode_sigen_ai_mode()
    # response = await sigen.set_operational_mode_tou()
    # response = await sigen.set_operational_mode_fully_fed_to_grid()
    # response = await sigen.set_operational_mode_maximum_self_powered()
    # logger.info(f"Response: {response}")

    # logger.info("\nFetching current operational mode...")
    # current_mode = await sigen.get_operational_mode()
    # logger.info(f"Current Operational Mode: {current_mode}")


if __name__ == "__main__":
    asyncio.run(main())