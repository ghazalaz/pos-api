<h1>POS API</h1>

This repository contains two django prjects.
<ul>
<li>demo: API for point of sale system with CRUD operation for menuItems and orders </li>
<li>demo2: An extention of demo with modifier groups and modifiers </li>
</ul>
<h2>Installation</h2>

git clone git@github.com:ghazalaz/pos-api.git
</br></br>
cd PROJECT_NAME
</br></br>
./runserver.sh
</br></br>

admin login info: {"username": "admin", "password": "toor"}

<h1>Examples</h1>


`POST,GET /api/v1/menu-items/` `GET, PUT, DELETE /api/v1/menu-items/id/`

```
{
    "name": "Burger",
    "price": 10,
    "quantity": 7,
    "description": ""
}
```
<h3>demo</h3>
</br>

`POST, GET /api/v1/orders/` `GET, PUT, DELETE /api/v1/orders/id/`

```
{
    "items": [
    {
        "menu_item": 2,
        "quantity": 5
    },
    {
        "menu_item": 3,
        "quantity": 10
    }],
    "paid": 150,
    "note": "!"
}
```

<h3>demo2</h3>
</br>

`POST, GET /api/v1/modifier/groups/` `GET, PUT, DETELE /api/v1/modifier/groups/id/`

```
{
    "name": "Toppings"
}
{
    "name": "Bun Choice"
}
```

`POST, GET /api/v1/modifier/items` `GET, PUT, DELETE /api/v1/modifier/items/id/`


```
create one
{
    "name": "Lettuce",
    "group": 1
}
create multiple
[
{
    "name": "Onion",
    "group": 1
},
{
    "name": "Pickles",
    "group": 1
},
{
    "name": "Keto",
    "group": 2
},
]
```

`POST, GET /api/v1/orders/` `GET, PUT, DELETE /api/v1/orders/id/` 

```
{
    "items": [
		{
			"menu_item": 1,
			"quantity": 5,
			"modifiers_list": [{"group":1,"items":[2]}, {"group":2,"items":[11,12]}]
		},
		{
			"menu_item": 2,
			"quantity": 7,
			"modifiers_list": [{"group":1,"items":[2]}]
		}
	],
    "paid": 200,
    "note": "Thanks"
}
```
