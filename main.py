"""
Program main entry file.
This file contains all the program constants, logic and rendering loop.
Handles all input from the user and draws everything on the screen using the pygame library.
"""

import graphs
import graphics
import files
import time
import pygame
from pygame.locals import *
import utils

TITLE = "Shortest path tree in unweighted graphs"
MAIN_WINDOW_HEIGHT = 1000 # fixed height
MAIN_WINDOW_WIDTH = 1500 # fixed width
MAIN_WINDOW_BACKGROUND_COLOR = (255, 255, 255) # currently white

UI_BAR_HEIGHT = 75
UI_BAR_COLOR = (128, 128, 128) # currently grey
UI_BUTTON_COLOR_NOT_PRESSED = (200, 200, 200) # currently light grey
UI_BUTTON_COLOR_PRESSED = (50, 50, 50)# currently dark grey
UI_BUTTON_TEXT_COLOR = (50, 50, 50)# currently dark grey
UI_BUTTON_TEXT_RIGHT_SHIFT = 20
UI_BUTTON_TEXT_DOWN_SHIFT = 10
NEW_BUTTON_POSITION = (12.5, 12.5, 125, 50)
SAVE_BUTTON_POSITION = (160, 12.5, 125, 50)
LOAD_BUTTON_POSITION = (307.5, 12.5, 125, 50)
EXIT_BUTTON_POSITION = (1362.5, 12.5, 125, 50)

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
    main_window = pygame.display.set_mode((MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    # font info
    sysfont = pygame.font.get_default_font()
    font = pygame.font.SysFont(None, graphics.VERTEX_KEY_TEXT_SIZE) 

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

    # creating all the buttons in the ui bar
    newButton = graphics.buttonObject("New", NEW_BUTTON_POSITION, UI_BUTTON_COLOR_NOT_PRESSED)
    saveButton = graphics.buttonObject("Save", SAVE_BUTTON_POSITION, UI_BUTTON_COLOR_NOT_PRESSED)
    loadButton = graphics.buttonObject("Load", LOAD_BUTTON_POSITION, UI_BUTTON_COLOR_NOT_PRESSED)
    exitButton = graphics.buttonObject("Exit", EXIT_BUTTON_POSITION, UI_BUTTON_COLOR_NOT_PRESSED)

    # create and fill the list of all the buttons in the ui bar
    uiObjects = []
    uiObjects.append(newButton)
    uiObjects.append(saveButton)
    uiObjects.append(loadButton)
    uiObjects.append(exitButton)

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

                    # user pressed under the ui bar
                    if mouse_position[1] > UI_BAR_HEIGHT:

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
                                verteciesObjects.append(graphics.vertexObject(graphics.VERTEX_CIRCLE_COLOR, (mouse_position), new_vertex))
                                G.add_vertex(new_vertex)

                    # user pressed on the ui bar
                    else:
                         for o in uiObjects:
                            # check if pressed on a button
                            if o.position[0] < mouse_position[0] and mouse_position[0] < (o.position[0] + o.position[2]) and o.position[1] < mouse_position[1] and mouse_position[1] < (o.position[1] + o.position[3]):
                                o.color = UI_BUTTON_COLOR_PRESSED

                                # reset the current graph
                                if o.text == "New":
                                    G = graphs.Graph()
                                    verteciesObjects.clear()
                                    edgesObjects.clear()
                                    new_edge_start_vertex = None
                                    new_edge_end_vertex = None

                                # open save file dialog
                                elif o.text == "Save":
                                    files.saveFile(G, verteciesObjects, edgesObjects)
                                    
                                # open load file dialog
                                elif o.text == "Load":
                                    result = files.loadSave()
                                    G.V.clear()
                                    G.E.clear()
                                    verteciesObjects.clear() 
                                    # create the new graph
                                    for s in result[0]:
                                        G.add_vertex(graphs.Vertex(s))
                                    for s in result[1]:
                                        G.add_edge(graphs.Edge(utils.findVertexByKey(G, s[0]), utils.findVertexByKey(G, s[1])))
                                    for s in result[2]:
                                        ve = None
                                        for v in G.V:
                                            if v.key == s[2]:
                                                ve = v
                                        verteciesObjects.append(graphics.vertexObject(graphics.VERTEX_CIRCLE_COLOR, (s[1][0], s[1][1]), ve))
                                    edgesObjects.clear()
                                    for e in G.E:
                                        edgesObjects.append(graphics.edgeObject(e, EDGE_COLOR))

                                # close the program
                                elif o.text == "Exit":
                                    running = False
                                
                    # update the last time the user pressed the screen as the current time
                    # used for checking if the user double clicked
                    last_click_time = current_time

                # middle mouse click
                elif event.button == 2:

                    # reset vertecies and edges colors in case user already ran the algorithm
                    for v in verteciesObjects:
                        v.color = graphics.VERTEX_CIRCLE_COLOR
                    for e in edgesObjects:
                        e.color = EDGE_COLOR

                    for v in verteciesObjects:
                        distance = pygame.Vector2(v.position).distance_to(pygame.Vector2(mouse_position))
                        # user pressed on an existing vertex, run BFS
                        if distance < graphics.VERTEX_CIRCLE_RADIUS:
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
                        if distance < graphics.VERTEX_CIRCLE_RADIUS:
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
                                    v.color = graphics.VERTEX_CIRCLE_COLOR
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
                                    new_edge_start_vertex.color = graphics.VERTEX_CIRCLE_COLOR
                                    new_edge_start_vertex = None
                                    new_edge_end_vertex = None
            
            # user pressed a keyboard key
            elif event.type == pygame.KEYDOWN:
                # handling screen movement (technicly we move the objects on the screen)
                if event.key is pygame.K_w:
                    for v in verteciesObjects:
                        v.position = (v.position[0], v.position[1] + MOVEMENT_SHIFT)
                elif event.key is pygame.K_s:
                    for v in verteciesObjects:
                        v.position = (v.position[0], v.position[1] - MOVEMENT_SHIFT)
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
                    pygame.draw.circle(main_window, v.color, v.position, graphics.VERTEX_CIRCLE_RADIUS)  
                    # draw text inside the circle with the vertex key as value
                    img = font.render(v.vertexInfo.key, True, graphics.VERTEX_KEY_TEXT_COLOR)    
                    main_window.blit(img, (v.position[0] - 12.5, v.position[1] - 12.5)) 

            # drawing the user interface

            # draw ui bar
            pygame.draw.rect(main_window, UI_BAR_COLOR, (0, 0, MAIN_WINDOW_WIDTH, UI_BAR_HEIGHT))

            # draw all the buttons
            for o in uiObjects:
                pygame.draw.rect(main_window, o.color, o.position)
                img = font.render(o.text, True, UI_BUTTON_TEXT_COLOR)    
                main_window.blit(img, (o.position[0] + UI_BUTTON_TEXT_RIGHT_SHIFT, o.position[1] + UI_BUTTON_TEXT_DOWN_SHIFT)) 
                # reset button color, needed in case it was pressed and its color was changed
                o.color = UI_BUTTON_COLOR_NOT_PRESSED

            # ---------- End of rendering ---------- #
                
            pygame.display.update()

    # ---------- end of program loop ---------- #

    pygame.quit()

if __name__ == "__main__":
  main()