from backend.db import get_db_connection
import utils.queries as queries
from datetime import datetime
import os

class Listing:
    def __init__(self, id, title, description, street_address, city, state, postal_code, country,
             price, bedroom_count, bathroom_count, furnished=False, pets_allowed=False,
             utilities_included=False, type=None, date_listed=None):
        self.id = id
        self.title = title
        self.description = description
        self.street_address = street_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.price = price
        self.bedroom_count = bedroom_count
        self.bathroom_count = bathroom_count
        self.furnished = furnished
        self.pets_allowed = pets_allowed
        self.utilities_included = utilities_included
        self.type = type  # New property type field
        self.date_listed = date_listed if date_listed else datetime.now()


    @staticmethod
    def get_by_id(listing_id):  # Get listing by ID
        params = (listing_id,)
        listing_data = queries.execute_query_with_results(queries.GET_LISTING_BY_ID, params, dictionary=True, fetch_one=True)
        if listing_data:
            return Listing(
                id=listing_data['id'],
                title=listing_data['title'],
                description=listing_data['description'],
                street_address=listing_data['street_address'],
                city=listing_data['city'],
                state=listing_data['state'],
                postal_code=listing_data['postal_code'],
                country=listing_data['country'],
                price=listing_data['price'],
                bedroom_count=listing_data['bedroom_count'],
                bathroom_count=listing_data['bathroom_count'],
                furnished=listing_data['furnished'],
                pets_allowed=listing_data['pets_allowed'],
                utilities_included=listing_data['utilities_included'],
                type=listing_data['type'],  # Added property_type
                date_listed=listing_data['created_at']
            )
        return None


    @staticmethod
    def get_all():  # Get all listings
        listings_data = queries.execute_query_with_results(queries.GET_ALL_LISTINGS, dictionary=True)
        listings = []
        for listing_data in listings_data:
            listings.append(Listing(
                id=listing_data['id'],
                title=listing_data['title'],
                description=listing_data['description'],
                street_address=listing_data['street_address'],
                city=listing_data['city'],
                state=listing_data['state'],
                postal_code=listing_data['postal_code'],
                country=listing_data['country'],
                price=listing_data['price'],
                bedroom_count=listing_data['bedroom_count'],
                bathroom_count=listing_data['bathroom_count'],
                furnished=listing_data['furnished'],
                pets_allowed=listing_data['pets_allowed'],
                utilities_included=listing_data['utilities_included'],
                type=listing_data['type'],  # Added property_type
                date_listed=listing_data['date_listed']
            ))
        return listings


    def save(self):  # Save new listing to the database
        insert_query = """
            INSERT INTO listings (title, description, street_address, city, state, postal_code, country, 
                                price, bedroom_count, bathroom_count, furnished, pets_allowed, 
                                utilities_included, type, date_listed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            self.title, self.description, self.street_address, self.city, self.state, self.postal_code,
            self.country, self.price, self.bedroom_count, self.bathroom_count, self.furnished, 
            self.pets_allowed, self.utilities_included, self.type, self.date_listed
        )
        queries.execute_query(insert_query, params)


    def update(self):  # Update existing listing in the database
        update_query = """
            UPDATE listings 
            SET title = %s, description = %s, street_address = %s, city = %s, state = %s, postal_code = %s,
                country = %s, price = %s, bedroom_count = %s, bathroom_count = %s, furnished = %s,
                pets_allowed = %s, utilities_included = %s, type = %s, date_listed = %s
            WHERE id = %s;
        """
        params = (
            self.title, self.description, self.street_address, self.city, self.state, self.postal_code,
            self.country, self.price, self.bedroom_count, self.bathroom_count, self.furnished,
            self.pets_allowed, self.utilities_included, self.type, self.date_listed, self.id
        )
        queries.execute_query(update_query, params)


    def delete(self):  # Delete listing from the database
        delete_query = "DELETE FROM listings WHERE id = %s;"
        params = (self.id,)
        queries.execute_query(delete_query, params)


    @staticmethod
    def search(filters):  # Search listings with filters
        where_clauses = []
        params = []
        
        if filters.get('title'):
            where_clauses.append("title LIKE %s")
            params.append(f"%{filters['title']}%")
        if filters.get('price_min'):
            where_clauses.append("price >= %s")
            params.append(filters['price_min'])
        if filters.get('price_max'):
            where_clauses.append("price <= %s")
            params.append(filters['price_max'])
        if filters.get('city'):
            where_clauses.append("city = %s")
            params.append(filters['city'])
        if filters.get('type'):  # Added property_type filter
            where_clauses.append("type = %s")
            params.append(filters['type'])
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1"
        search_query = f"SELECT * FROM listings WHERE {where_clause};"
        
        listings_data = queries.execute_query_with_results(search_query, params, dictionary=True)
        listings = []
        for listing_data in listings_data:
            listings.append(Listing(
                id=listing_data['id'],
                title=listing_data['title'],
                description=listing_data['description'],
                street_address=listing_data['street_address'],
                city=listing_data['city'],
                state=listing_data['state'],
                postal_code=listing_data['postal_code'],
                country=listing_data['country'],
                price=listing_data['price'],
                bedroom_count=listing_data['bedroom_count'],
                bathroom_count=listing_data['bathroom_count'],
                furnished=listing_data['furnished'],
                pets_allowed=listing_data['pets_allowed'],
                utilities_included=listing_data['utilities_included'],
                type=listing_data['type'],  # Added property_type
                date_listed=listing_data['date_listed']
            ))
        return listings
    
    def insert_image(self, image_data):
        if image_data is None:
            print("No image data provided.")
            return False
        
        if (queries.execute_query(queries.INSERT_NEW_LISTING_IMAGE, (self.id, image_data))):
            return True
        
        print("Error inserting image.")
        return False

    def insert_image_by_url(self, image_url):
        image_data = None

        if os.path.exists(image_url):
            with open(image_url, 'rb') as image_file:
                image_data = image_file.read()
        else:
            print(f"Image file {image_url} not found.")
            return False

        return self.insert_image(image_data)

    def get_images(self):
        if self.id is None:
            print("Listing ID is required to get images.")
            return None
        
        images_data = queries.execute_query_with_results(queries.GET_LISTING_IMAGES_BY_LISTING_ID, (self.id,), dictionary=True)

        images = []
        for image_data in images_data:
            images.append({
                'id': image_data['id'],
                'listing_id': image_data['listing_id'],
                'image_data': image_data['image_data']
            })
        return images
    
    def delete_images(self):
        if self.id is None:
            print("Listing ID is required to delete images.")
            return False
        
        if(queries.execute_query(queries.DELETE_LISTING_IMAGES_BY_LISTING_ID, (self.id,))):
            return True
        
        print("Error deleting images.")
        return False
    
    def delete_image(self, image_id):
        if image_id is None:
            print("Image ID is required to delete an image.")
            return False
        
        if(queries.execute_query(queries.DELETE_LISTING_IMAGE, (image_id,))):
            return True
        
        print("Error deleting image.")
        return False
    
    def get_image(self, image_id):
        if image_id is None:
            print("Image ID is required to get an image.")
            return None
        
        image_data = queries.execute_query_with_results(queries.GET_LISTING_IMAGE_BY_ID, (image_id,), dictionary=True, fetch_one=True)
        
        if image_data:
            return {
                'id': image_data['id'],
                'listing_id': image_data['listing_id'],
                'image_data': image_data['image_data']
            }
        return None
    
    def update_image(self, image_id, image_data):
        if image_id is None:
            print("Image ID is required to update an image.")
            return False
        
        if image_data is None:
            print("No image data provided.")
            return False
        
        if(queries.execute_query(queries.UPDATE_LISTING_IMAGE, ('image_data', image_data, image_id))):
            return True
        
        print("Error updating image.")
        return False
    
    def update_image_by_url(self, image_id, image_url):
        image_data = None

        if os.path.exists(image_url):
            with open(image_url, 'rb') as image_file:
                image_data = image_file.read()
        else:
            print(f"Image file {image_url} not found.")
            return False

        return self.update_image(image_id, image_data)
    