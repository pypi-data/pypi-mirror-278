## API 🚀

🎉 Introducing **API** for Countries States Cities Database.

### 📦 Installation

```bash
pip install py-countries-states-cities-database
```

### 📚 Usage

```python
    from py_countries_states_cities_database import (
        get_all_cities,
        get_all_states,
        get_all_countries,
        get_all_sub_regions,
        get_all_regions,
        get_all_states_and_cities_nested,
        get_all_countries_and_states_nested,
        get_all_countries_and_cities_nested,
        get_file_path
    )

    # All functions return a list of dictionaries
    print(get_all_cities())
    print(get_all_states())
    print(get_all_countries())
    print(get_all_sub_regions())
    print(get_all_regions())
    print(get_all_states_and_cities_nested())
    print(get_all_countries_and_states_nested())
    print(get_all_countries_and_cities_nested())


    # File name options
    | "cities.json"
    | "states.json"
    | "countries.json"
    | "subregions.json"
    | "regions.json"
    | "countries+cities.json"
    | "countries+states.json"
    | "states+cities.json"
    | "countries+states+cities.json",

    # Get the file path
    print(get_file_path("cities.json"))
```
