from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind =  engine)
session = DBSession()

# # code to insert Restaurant info
# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()
# session.query(Restaurant).all()

# # code to insert MenuItem info

# cheesepizza = MenuItem(name="Cheese Pizza", description = "Made with all cheese", course="Entree", price="$8.99", restaurant= myFirstRestaurant)
# session.add(cheesepizza)
# session.commit()
# session.query(MenuItem).all()


# code to read all Restaurants
restaurants = session.query(Restaurant).all()
MenuItems = session.query(MenuItem).all()

print "==================Restaurant================================="
for restaurant in restaurants:
    print restaurant.name

print "==================Items================================="
for item in MenuItems:
    print item.name

print "==================Veggie Burger================================="
veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

    # updating all veggieBurger to $2.99
    # if veggieBurger.price != 2.99:
    #     veggieBurger.price = '$2.99'
    #     session.add(veggieBurger)
    #     session.commit()


print "==================Urban Burger================================="
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=10).one()
print UrbanVeggieBurger.price
# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()

# print "==================Delete Spinach Ice Cream================================="
# spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
# print spinach.restaurant.name
# session.delete(spinach)
# session.commit()