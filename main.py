"""
Program main entry file.
This file contains all the program constants, logic and rendering loop.
Handles all input from the user and draws everything on the screen using the pygame library.
"""

import graphs
import graphics
import time
import pygame
from pygame.locals import *
import string
import math

TITLE = "Shortest path tree in unweighted graphs"
MAIN_WINDOW_HEIGHT = 1500 # fixed height
MAIN_WINDOW_WIDTH = 1000 # fixed width
MAIN_WINDOW_BACKGROUND_COLOR = (255, 255, 255) # currently white

VERTEX_CIRCLE_RADIUS = 45
VERTEX_CIRCLE_COLOR = (0, 0, 0) # currently black
VERTEX_KEY_TEXT_COLOR = (255, 255, 255) # currently white
VERTEX_KEY_TEXT_SIZE = 48
SELECTED_VERTEX_CIRCLE_COLOR = (0, 0, 255) # currently blue
SOURCE_VERTEX_CIRCLE_COLOR = (255, 204, 0) # currently orange
VERTEX_IN_BFS_COLOR = (102, 204, 0) # currently green

EDGE_IN_BFS_COLOR = (102, 204, 0) # currently green
EDGE_COLOR = (0, 0, 0) # currently black
EDGE_THICKNESS = 10

DOUBLE_CLICK_THERSOLD = 0.2 # seconds
SAFE_DISTANCE_BETWEEN_VERTECIES = 125 # minimum distance between vertecies so they hide each other

MOVEMENT_SHIFT = 30 # how much do the objects on the screen move on each press

# main entry for program
def main():

    # ---------- staring the program ---------- #
    
    # setting up the game window
    pygame.init()
    main_window = pygame.display.set_mode((MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH))
    pygame.display.set_caption(TITLE)

    # font info
    sysfont = pygame.font.get_default_font()
    font = pygame.font.SysFont(None, VERTEX_KEY_TEXT_SIZE) 

    # holds the graph's info
    G = graphs.Graph()

    # holds all the graphics objects that represent vertecies and edges
    verteciesObjects = []
    edgesObjects = []

    # for handling double click from user
    last_click_time = 0

    # used for creating new edges
    new_edge_start_vertex =  None
    new_edge_end_vertex = None

    # ---------- program loop ---------- #
    running = True
    while running:

        # fill the main window background color
        main_window.fill(MAIN_WINDOW_BACKGROUND_COLOR)
        
        # handling events
        for event in pygame.event.get():
            # player quit program
            if event.type == pygame.QUIT:
                running = False

            # ---------- Handling user input ---------- #

            # mouse click
            elif event.type == MOUSEBUTTONDOWN:

                # get current mouse position
                mouse_position = event.pos

                # left mouse click
                if  event.button == 1:
                    # get the time when the user pressed the screen
                    current_time = time.time()

                    # check for a double click
                    if current_time - last_click_time <= DOUBLE_CLICK_THERSOLD:

                        pressed_on_vertex = 0 # did the user pressed on a existing vertex

                        # check every vertex on the screen if the user tried to create a new one in its space
                        for v in verteciesObjects:
                            distance = pygame.Vector2(v.position).distance_to(pygame.Vector2(mouse_position))
                            # user pressed too close to an existing vertex
                            if distance < SAFE_DISTANCE_BETWEEN_VERTECIES:
                                pressed_on_vertex = 1

                        # user choose a good place for a new vertex
                        if pressed_on_vertex == 0:
                            # create and add a new vertex to the screen
                            new_vertex = graphs.Vertex(chr(ord('@')+len(verteciesObjects)+1))
                            verteciesObjects.append(graphics.vertexObject(VERTEX_CIRCLE_COLOR, (mouse_position), new_vertex))
                            G.add_vertex(new_vertex)

                    # update the last time the user pressed the screen as the current time
                    # used for checking if the user double clicked
                    last_click_time = current_time

                # middle mouse click
                elif event.button == 2:

                    # reset vertecies and edges colors in case user already ran the algorithm
                    for v in verteciesObjects:
                        v.color = VERTEX_CIRCLE_COLOR
                    for e in edgesObjects:
                        e.color = EDGE_COLOR
                    
                    for v in verteciesObjects:
                        distance = pygame.Vector2(v.position).distance_to(pygame.Vector2(mouse_position))
                        # user pressed on an existing vertex, run BFS
                        if distance < VERTEX_CIRCLE_RADIUS:
                            v.color = SOURCE_VERTEX_CIRCLE_COLOR
                            result = graphs.BFS(G, v.vertexInfo)
                            # paint vertecies in BFS tree (exept source) in green
                            for i in result:
                                # paint all the vertecies that are in the BFS tree in green
                                if i.visited is True and i.v is not v.vertexInfo:
                                    for vo in verteciesObjects:
                                        if vo.vertexInfo.key is i.v.key:
                                            vo.color = VERTEX_IN_BFS_COLOR
                                # paint all the edges that are in the BFS tree in green
                                for e in edgesObjects:
                                    if ((e.edgeInfo.start is i.v and e.edgeInfo.end is i.previous) or (e.edgeInfo.end is i.v and e.edgeInfo.start is i.previous)) and i.visited is True:
                                        e.color = EDGE_IN_BFS_COLOR


                # right mouse click
                elif event.button == 3:
                    # check if the user pressed on a vertex
                    for v in verteciesObjects:
                        distance = pygame.Vector2(v.position).distance_to(pygame.Vector2(mouse_position))
                        # user pressed on an existing vertex
                        if distance < VERTEX_CIRCLE_RADIUS:
                            # select vertex as a starting point for a new edge
                            if new_edge_start_vertex is None:
                                new_edge_start_vertex = v
                                # set the selected vertex color to blue so the user will know what he pressed
                                v.color = SELECTED_VERTEX_CIRCLE_COLOR
                            else:
                                # select vertex as an ending point for a new edge
                                new_edge_end_vertex = v
                                valid = True
                                # check if user tries to create an edge from a vertex to himself,
                                # if so reset the first vertex the user selected
                                if new_edge_start_vertex is new_edge_end_vertex:
                                    v.color = VERTEX_CIRCLE_COLOR
                                    new_edge_start_vertex = None
                                    new_edge_end_vertex = None
                                    valid = False
                                else:
                                    # check if the edge the user wants to create exists already
                                    for e in edgesObjects:
                                        if (e.edgeInfo.start is new_edge_start_vertex.vertexInfo and e.edgeInfo.end is new_edge_end_vertex.vertexInfo) or \
                                                (e.edgeInfo.end is new_edge_start_vertex.vertexInfo and e.edgeInfo.start is new_edge_end_vertex.vertexInfo):
                                            valid = False
                                            continue
                                # create the new edge
                                if valid is True:
                                    new_edge = graphs.Edge(new_edge_start_vertex.vertexInfo, new_edge_end_vertex.vertexInfo)
                                    edgesObjects.append(graphics.edgeObject(new_edge, EDGE_COLOR))
                                    G.add_edge(new_edge)
                                    new_edge_start_vertex.color = VERTEX_CIRCLE_COLOR
                                    new_edge_start_vertex = None
                                    new_edge_end_vertex = None
            
            # user pressed a keyboard key
            elif event.type == pygame.KEYDOWN:
                # reset the window
                if event.key is pygame.K_r:
                    G = graphs.Graph()
                    verteciesObjects.clear()
                    edgesObjects.clear()
                    new_edge_start_vertex = None
                    new_edge_end_vertex = None

                # handling screen movement (technicly we move the objects on the screen)
                elif event.key is pygame.K_w:
                    for v in verteciesObjects:
                        v.position = (v.position[0], v.position[1] - MOVEMENT_SHIFT)
                elif event.key is pygame.K_s:
                    for v in verteciesObjects:
                        v.position = (v.position[0], v.position[1] + MOVEMENT_SHIFT)
                elif event.key is pygame.K_a:
                    for v in verteciesObjects:
                        v.position = (v.position[0] - MOVEMENT_SHIFT, v.position[1])
                elif event.key is pygame.K_d:
                    for v in verteciesObjects:
                        v.position = (v.position[0] + MOVEMENT_SHIFT, v.position[1])

            # ---------- End of handling user input ---------- #

            # ---------- Rendering ---------- #

            # draw edges on the main screen
            # we want to draw the edges before the vertecies so they will be under them
            for e in edgesObjects:
                # get start and end position for the edge
                for v in verteciesObjects:
                    if v.vertexInfo.key is e.edgeInfo.start.key:
                        start_pos = v.position
                    elif v.vertexInfo.key is e.edgeInfo.end.key:
                        end_pos = v.position
                pygame.draw.line(main_window, e.color, start_pos, end_pos, EDGE_THICKNESS)

            # draw vertecies on the main window
            for v in verteciesObjects:
                    # draw circle
                    pygame.draw.circle(main_window, v.color, v.position, VERTEX_CIRCLE_RADIUS)  
                    # draw text inside the circle with the vertex key as value
                    img = font.render(v.vertexInfo.key, True, VERTEX_KEY_TEXT_COLOR)    
                    main_window.blit(img, (v.position[0] - 12.5, v.position[1] - 12.5)) 

            # ---------- End of rendering ---------- #
                
            pygame.display.update()

    # ---------- end of program loop ---------- #

    pygame.quit()

if __name__ == "__main__":
  main()
  