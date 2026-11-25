import math
from .exceptions import InvalidPackError, InvalidPackQuantityError, InvalidStayDurationError

class Pack:
    default_note = "per person"

    def __init__(self, pack_id, name, category, price, summary, inclusions, price_note=None):
        if price < 0:
            raise InvalidPackError("Pack price cannot be negative.")
        self.pack_id = pack_id
        self.name = name
        self.category = category
        self._price = price
        self.summary = summary
        self.inclusions = inclusions
        self.price_note = price_note or self.default_note

    @property
    def price(self):
        return self._price

    @property
    def formatted_price(self):
        return f"₱{self._price:,}"

    def check_inputs(self, people, nights):
        if not isinstance(people, int) or people < 1:
            raise InvalidPackQuantityError("Number of people must be at least 1.")
        if not isinstance(nights, int) or nights < 1:
            raise InvalidStayDurationError("Number of nights must be at least 1.")

    def calculate_cost(self, people, nights=1):
        raise NotImplementedError("Use PerPersonPack, PerMorningPack or PerGroupPack.")   

# Same price for every person, once per stay
class PerPersonPack(Pack):
    def calculate_cost(self, people, nights=1):
        self.check_inputs(people, nights)
        return self.price * people

# Breakfast: price per person for every morning of the stay
class PerMorningPack(Pack):
    default_note = "per person / per morning"

    def calculate_cost(self, people, nights=1):
        self.check_inputs(people, nights)
        return self.price * people * nights
    
# One price for each group of up to "group_size" people
class PerGroupPack(Pack):
    default_note = "per group"

    def __init__(self, *args, group_size=6, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_size = group_size

    def calculate_cost(self, people, nights=1):
        self.check_inputs(people, nights)
        groups = math.ceil(people / self.group_size)
        return self.price * groups

class PackCatalog:
    CATEGORIES = [
        ("adventure", "Adventure"),
        ("wellness", "Wellness"),
        ("dining", "Dining"),
        ("leisure", "Leisure"),
    ]

    def __init__(self):
        self.packs = [
            PerPersonPack("stargazing", "Celestial Stargazing Pack", "adventure", 2800,
                          "After-hours Observatory Deck and guided telescope",
                          ["Exclusive after-hours access to the Mountaintop Observatory Deck",
                           "High-powered celestial telescope rental with guided constellation mapping",
                           "Heated fleece blanket & insulated thermal lounge seating",
                           "Complimentary artisanal hot cocoa or spiced herbal tea"]),
            PerPersonPack("canopy-expedition", "Canopy Expedition", "adventure", 4500,
                          "Guided high-altitude hanging rope-bridge tour",
                          ["Guided high-altitude hanging rope-bridge tour",
                           "4K drone videography & photography session (digital copies included)",
                           "Weatherproof technical gear rental (harness, helmet, and waterproof shell)",
                           "Commemorative waterproof trail map print & hydration flask"]),
            PerPersonPack("ridge-river-trek", "Ridge & River Trek Pack", "adventure", 3800,
                          "Sunrise ridge hike and bamboo river rafting",
                          ["Guided sunrise valley ridge hike",
                           "Private bamboo river-rafting excursion along the forest gorge",
                           "Gourmet eco-packed trail lunch box & electrolyte refreshments",
                           "Dry-bag rental and post-trek towel service"]),
            PerPersonPack("thermal-spa", "Forest Thermal Spa Pack", "wellness", 5200,
                          "Forest stream access and river-stone massage",
                          ["Private access to the natural mountain forest stream",
                           "60-minute heated river-stone full-body massage session",
                           "Unlimited aromatherapy moss steam room pass",
                           "Organic linen robe, bamboo slippers, and botanical skincare kit"]),
            PerPersonPack("hydro-spa", "Canopy Infinity Hydro-Spa Pack", "wellness", 3500,
                          "Glass-bottom infinity pool and hydrotherapy circuit",
                          ["All-day access to the cantilevered glass-bottom infinity pool",
                           "Heated mineral hydrotherapy jet circuit pass",
                           "2-hour reserved floating lounge bed",
                           "Two complimentary cold-pressed organic detox juices"]),
            PerMorningPack("continental-breakfast", "Artisanal Continental Breakfast", "dining", 950,
                           "Fresh pastries, granola and single-origin coffee",
                           ["Freshly baked viennoiserie & sourdough pastries",
                            "Granola, organic yogurt, artisan cheeses, and seasonal tropical fruits",
                            "Single-origin brewed coffee, loose-leaf tea, or fresh fruit juice"]),
            PerMorningPack("grand-breakfast", "Lushiux Grand Breakfast Buffet", "dining", 1500,
                           "Skyview Dining Hall with live bakery and omelet station",
                           ["Unlimited access to the Skyview Dining Hall",
                            "Live artisanal bakery & made-to-order egg/omelet station",
                            "Gourmet pancake, waffle, and French toast bar with local honey",
                            "International & local hot entrees, smoked salmon, and cold cuts",
                            "Freshly squeezed tropical juice bar & barista-crafted espresso drinks"]),
            PerGroupPack("karaoke-pod", "Canopy Glass Karaoke Pod", "leisure", 2200,
                         "Glass pod in the canopy, up to 6 guests",
                         ["Private access to a soundproofed glass pod suspended in the forest canopy",
                          "75-inch 4K OLED display with surround-sound spatial audio",
                          "Dual studio-grade wireless microphones & cloud-updated global song library",
                          "Complimentary bar snack platter & welcome mocktails for up to 6 guests"],
                         price_note="per group / 2 hours", group_size=6),
            PerPersonPack("gaming-lounge", "Executive Gaming Lounge Pass", "leisure", 1500,
                          "Liquid-cooled PC rigs, PS5 and Xbox Series X",
                          ["Access to the private, sound-insulated Lushiux Gaming Suite",
                           "High-end liquid-cooled PC rigs (RTX-series GPUs, 240Hz monitors) & next-gen consoles (PS5 / Xbox Series X)",
                           "Ergonomic pro-tier gaming chairs & noise-canceling surround headsets",
                           "High-speed dedicated fiber line & complimentary energy drinks/snacks"],
                          price_note="per person / 3 hours"),
        ]

    def all(self):
        return self.packs

    def get(self, pack_id):
        for pack in self.packs:
            if pack.pack_id == pack_id:
                return pack
        raise InvalidPackError(f"Pack '{pack_id}' does not exist.")

    def by_category(self, category):
        category = (category or "all").strip().lower()
        if category == "all":
            return self.packs
        if category not in [key for key, label in self.CATEGORIES]:
            raise InvalidPackError(f"Unknown pack category: '{category}'.")
        return [pack for pack in self.packs if pack.category == category]
    
    # Adds all chosen packs         selections = {pack_id: number_of_people}
    def price_selection(self, selections, nights):
        lines = []
        total = 0
        for pack_id, people in selections.items():
            pack = self.get(pack_id)
            cost = pack.calculate_cost(people, nights)
            lines.append({"pack": pack, "people": people, "cost": cost})
            total += cost
        return lines, total