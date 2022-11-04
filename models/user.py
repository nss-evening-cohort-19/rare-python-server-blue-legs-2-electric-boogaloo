class User:
    """User Class"""
    def __init__(self, id, first_name, last_name, email, bio,username, password, profile_image_url, created_on, active):
    
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.profile_image_url = profile_image_url
        self.created_on = created_on
        self.active = active
    
    def first_last(self):
        """Returns first and last name"""
        return{
            "first_name": self.first_name,
            "last_name": self.last_name
            }
        