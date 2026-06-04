import time
import random
import logging
import numpy as np

# Configure logging
logger = logging.getLogger("DrillSoftEngine")
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class DrillSoftMechanics:
    """
    Physical Simulation Layer representing Heavy Energy Telemetry.
    Computes Torque & Drag, and Transient Influx Envelopes (IME).
    """
    def __init__(self):
        self.axial_tension = 150.0  # klbs
        self.hook_load = 200.0      # klbs
        self.surface_pressure = 800 # psi
        self.influx_volume = 0.0    # bbl
        
    def generate_telemetry_tick(self) -> dict:
        """
        Simulates 10 seconds of physical rig operation.
        Occasionally spawns a 'Multiphase Kick' (Influx).
        """
        # Normal drilling perturbations
        self.axial_tension += random.uniform(-2.0, 2.0)
        self.hook_load += random.uniform(-1.5, 1.5)
        
        kick_probability = random.random()
        is_kick = False
        
        # 10% chance of a pressure transient (Multiphase Kick)
        if kick_probability > 0.90:
            is_kick = True
            logger.warning("🚨 TRANSIENT INFLUX DETECTED! Multiphase kick mechanics initiated.")
            self.surface_pressure += random.uniform(50.0, 200.0)
            self.influx_volume += random.uniform(1.0, 5.0)
        else:
            # Bleed off if normal
            self.surface_pressure = max(800.0, self.surface_pressure - 10.0)
            self.influx_volume = max(0.0, self.influx_volume - 0.5)

        return {
            "timestamp": time.time(),
            "axial_tension_klbs": round(self.axial_tension, 2),
            "hook_load_klbs": round(self.hook_load, 2),
            "surface_pressure_psi": round(self.surface_pressure, 2),
            "influx_volume_bbl": round(self.influx_volume, 2),
            "pressure_spike": is_kick
        }
