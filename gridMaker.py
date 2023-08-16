import geopy.point
import geopy

def gridMaker(center: geopy.point.Point, \
              top_left: geopy.point.Point, \
              bottom_right: geopy.point.Point, \
              x_step: float, \
              y_step: float) -> list[tuple[float,float]]:    
    
    """Returns a grid of points where center, top_left, and bottom_right are three of the four vertexes 
    of the parallelogram. step_x and step_y are the distance between the points in the grid.
    
    Args:
        center (Point): A vertex of the grid/parallelogram
        top_left (Point): A vertex of the grid/parallelogram
        bottom_right (Point): A vertex of the grid/parallelogram
        x_step (float): Distance between points in the x axis of the grid/parallelogram. The
                        x axis is the one defined by the center and the bottom_right points
        y_step (float): Distance between points in the x axis of the grid/parallelogram. The
                        x axis is the one defined by the center and the bottom_right points

    Returns:
        list[tuple[float,float]]: The grid. List of tuples. Each tuple are the latitude and
                                  the longitude of a point in the grid
    """    

    # Compute vector_x and vector_y coordinates
    vector_x_lat = bottom_right.latitude - center.latitude
    vector_x_lon = bottom_right.longitude - center.longitude
    vector_y_lat = top_left.latitude - center.latitude
    vector_y_lon = top_left.longitude - center.longitude

    # Compute the number of points in the grid according to the steps
    vx_norm = geopy.distance.geodesic(center, bottom_right).kilometers
    vy_norm = geopy.distance.geodesic(center, top_left).kilometers
    num_points_x = vx_norm/x_step
    num_points_y = vy_norm/y_step

    # Compute the grid of points
    grid = [] 
    for i in range(num_points_x):
        for j in range(num_points_y):
            latitude = center.latitude + \
                       (i/(num_points_x-1))*vector_x_lat + \
                       (j/(num_points_y-1))*vector_y_lat
            longitude = center.longitude + \
                       (i/(num_points_x-1))*vector_x_lon + \
                       (j/(num_points_y-1))*vector_y_lon
            grid.append((latitude, longitude))
            
    return grid