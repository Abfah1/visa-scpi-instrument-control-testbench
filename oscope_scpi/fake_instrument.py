
import random
import time
import numpy as np

class FakeVisaInstrument:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.timeout = 5000
        print(f"FakeVisaInstrument: Opened {resource_name}")
        self._ieee_header = b'#800000010' # Example IEEE block header

    def write(self, cmd):
        print(f"FakeVisa: WRITE '{cmd}'")
        return len(cmd)

    def query(self, cmd):
        print(f"FakeVisa: QUERY '{cmd}'")
        if "*IDN?" in cmd:
            return "KEYSIGHT TECHNOLOGIES,MSO-X 3054A,MY54490123,10.00.2018021312"
        elif "SYSTem:ERRor?" in cmd:
            return "+0,No error"
        elif "WAVeform:PREamble?" in cmd:
            # Return a valid preamble for WORD format, Normal acquisition
            # Format: format, type, points, count, xinc, xorg, xref, yinc, yorg, yref
            # wav_form=2 (WORD), acq_type=1 (RAW/Normal), points=1000, count=1, ...
            return "2,1,1000,1,1.0E-6,0,0,0.01,0,32768,0,0,0,0,0,0,0,0,0,0,1,1,0,0"
        elif "WAVeform:SOURce?" in cmd:
            return "CHAN1"
        elif "WAVeform:VIEW?" in cmd:
            return "MAIN"
        elif "WAVeform:POINts:MODE?" in cmd:
            return "MAX"
        elif "WAVeform:POINts?" in cmd:
            return "1000"
        elif "DISPlay:DATA?" in cmd:
            # Should be handled by query_binary_values for block data
             return "#8000000100123456789" 
        elif "MEASure" in cmd:
            # Return a random number for measurements
            return f"{random.uniform(0, 5):.4E}"
        elif "STATus?" in cmd:
            return "1"
        
        return "0"

    def read_raw(self):
        # Only used if something calls read_raw directly
        return b""

    def query_binary_values(self, cmd, datatype='s', container=bytes):
        print(f"FakeVisa: QUERY_BINARY '{cmd}'")
        if "DISPlay:DATA?" in cmd:
            # Return a valid PNG header
            # 1x1 pixel PNG for simplicity or a small generated one?
            # Let's return a valid small placeholder PNG bytes
            # Minimal PNG signature
            return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        elif "WAVeform:DATA?" in cmd:
            # Generate sine wave data 
            # 1000 points of int16 (2 bytes each)
            t = np.linspace(0, 4*np.pi, 1000)
            y = 30000 * np.sin(t) # Scale to int16 range roughly
            data = y.astype(np.int16).tobytes()
            return data
            
        return b""

    def close(self):
        print("FakeVisaInstrument: Closed")

    def clear(self):
        pass
