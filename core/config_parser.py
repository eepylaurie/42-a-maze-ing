def parse_config(filename: str):
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=')
                key = key.strip().upper()
                value = value.strip()
                # Zahlen-Werte konvertieren
                if key in ['WIDTH', 'HEIGHT', 'SEED']:
                    config[key] = int(value)
                # Koordinaten-Paare (x,y) konvertieren
                elif key in ['ENTRY', 'EXIT']:
                    config[key] = tuple(map(int, value.split(',')))
        return config
    except Exception as e:
        print(f"Fehler beim Einlesen der Config: {e}")
        return None
