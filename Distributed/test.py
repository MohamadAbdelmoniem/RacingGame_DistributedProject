''' 

# Pickle the image data
image_data = pygame.image.tostring(players[player_id].image, "RGBA")
pickled_image = pickle.dumps(image_data)

# Unpickle the image data
unpickled_image = pickle.loads(pickled_image)
restored_image = pygame.image.fromstring(unpickled_image, image.get_size(), "RGBA")
    
'''