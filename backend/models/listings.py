from backend.db import get_db_connection
import utils.queries as queries
from datetime import datetime

class Listing:
    def __init__(self, id, title, description, street_address, city, state, postal_code, country,
                 price, bedroom_count, bathroom_count, furnished=False, pets_allowed=False,
                 utilities_included=False, property_type=None, date_listed=None):
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
        self.property_type = property_type
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
                property_type=listing_data['property_type'],
                date_listed=listing_data['date_listed']
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
                property_type=listing_data['property_type'],
                date_listed=listing_data['date_listed']
            ))
        return listings

    def save(self):  # Save new listing to the database
        insert_query = """
            INSERT INTO listings (title, description, street_address, city, state, postal_code, country, 
                                  price, bedroom_count, bathroom_count, furnished, pets_allowed, 
                                  utilities_included, property_type, date_listed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            self.title, self.description, self.street_address, self.city, self.state, self.postal_code,
            self.country, self.price, self.bedroom_count, self.bathroom_count, self.furnished, 
            self.pets_allowed, self.utilities_included, self.property_type, self.date_listed
        )
        queries.execute_query(insert_query, params)

    def update(self):  # Update existing listing in the database
        update_query = """
            UPDATE listings 
            SET title = %s, description = %s, street_address = %s, city = %s, state = %s, postal_code = %s,
                country = %s, price = %s, bedroom_count = %s, bathroom_count = %s, furnished = %s,
                pets_allowed = %s, utilities_included = %s, property_type = %s, date_listed = %s
            WHERE id = %s;
        """
        params = (
            self.title, self.description, self.street_address, self.city, self.state, self.postal_code,
            self.country, self.price, self.bedroom_count, self.bathroom_count, self.furnished,
            self.pets_allowed, self.utilities_included, self.property_type, self.date_listed, self.id
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
                property_type=listing_data['property_type'],
                date_listed=listing_data['date_listed']
            ))
        return listings
