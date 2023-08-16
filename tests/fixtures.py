MENU_DATA = {'title': 'Test Menu', 'description': 'Test Description'}
MENU_DATA_UPDATE = {'title': 'Test Menu updat',
                    'description': 'Test Description update'}
SUBMENU_DATA = {'title': 'Test SubMenu',
                'description': 'Test Description SubMenu'}
SUBMENU_DATA_UPDATE = {'title': 'Test SubMenu updat',
                       'description': 'Test SubMenu Description update'}
DISH_DATA = {'title': 'Test Dish',
             'description': 'Test Description Dish',
             'price': '150.50',
             'discount': 0}
DISH_DATA_UPDATE = {'title': 'Test Dish updat',
                    'description': 'Test Dish Description update',
                    'price': '170.99',
                    'discount': 0}
DISH_DATA2 = {'title': 'Test Dish2',
              'description': 'Test Description Dish2',
              'price': '250.50',
              'discount': 15}

ALL_DATA = {
    'Test Menu': {
        'Test SubMenu': {
            'Test Dish': {
                'description': 'Test Description Dish',
                'price': '150.50'
            },
            'Test Dish2': {
                'description': 'Test Description Dish2',
                'price': '250.50'
            },
            'description': 'Test Description SubMenu'
        },
        'description': 'Test Description'
    },
}

ALL_DATA_WITHOUT_DISH = {
    'Test Menu': {
        'Test SubMenu': {
            'Test Dish2': {
                'description': 'Test Description Dish2',
                'price': '250.50'
            },
            'description': 'Test Description SubMenu'
        },
        'description': 'Test Description'
    },
}
