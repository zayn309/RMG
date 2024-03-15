from utils import get_random_film,open_url_in_browser,load_svg
import pygame, sys
import pygame_gui
import threading

pygame.init()
pygame.font.init()
pygame.display.set_caption("RMG")
pygame.display.set_icon(pygame.image.load('assets\letterboxd-mac-icon.png'))

COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")
backGroundCol = "#14181c"
desc_color = "#99aabb"

SCREEN_WIDTH = 600
SCREEN_HIGHT = 900

BUTTON_WIDTH = 150
BUTTON_HIGHT = 40

gui_font = pygame.font.Font(None, 30)
textSur_font = pygame.font.SysFont(None, 28,)
filmName_font = pygame.font.Font("assets/TiemposHeadline-Black.ttf", 35)
smallFont = pygame.font.SysFont(None,22,)
imdb_font = pygame.font.SysFont("ArTarumianMHarvats",25,)
rating_font = pygame.font.SysFont(None,27,)
desc_font = pygame.font.SysFont("Arial",20,)


imdb_logo = imdb_font.render("IMDb",True,"#000000")
yts_logo = load_svg('assets/Logo-YTS.svg')
yts_logo = pygame.transform.scale(yts_logo,(52,26))
star = pygame.image.load('assets/star.png')
star = pygame.transform.scale(star,(28,28)) 

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))

film_info = None

class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#0d0d0d"

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = "#326a83"
        # text
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#5c9cc1"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            elif pygame.mouse.get_pressed()[2]:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = "#0d3249"
        return self.pressed

def draw_text(text, text_col, x, y,border_col,font,bg_co,init_x,init_y,draw_border = False):
    img = font.render(text, True, text_col)
    rect_out = None
    new_x = None
    new_y = None
    if draw_border:
        rect_out = pygame.rect.Rect(x ,y ,img.get_width() + 8,img.get_height() + 10 )
        if rect_out.x + rect_out.width > SCREEN_WIDTH - 2:
            new_x = init_x
            new_y = rect_out.y + rect_out.height - 23 
            return new_x,new_y 
        else:
            new_x = rect_out.x + rect_out.width + 14 
            new_y = init_y
        pygame.draw.rect(screen,border_col,rect_out,border_radius=3)
    rect_in = pygame.rect.Rect(x ,y ,img.get_width() ,img.get_height() )

    if draw_border:
        rect_in.center = rect_out.center
    pygame.draw.rect(screen,bg_co,rect_in,border_radius = 3)
    
    if not draw_border:
        pygame.draw.line(screen,"#445566",(rect_in.x - 1,rect_in.y + rect_in.height + 1),(rect_in.x + rect_in.width + 1,rect_in.y + rect_in.height + 1))

    screen.blit(img,rect_in)

    return new_x, new_y

def draw_movie_name(name,y):
    name = filmName_font.render(name + ' (' + film_info['release_year'] + ')',True, "#FFFFFF",backGroundCol)
    if name.get_width() > SCREEN_WIDTH - 40:
        name = pygame.transform.scale_by(name,(SCREEN_WIDTH- 40) / name.get_width() * 1.0)
    name_rect = name.get_rect(center = (SCREEN_WIDTH //2,y ))
    screen.blit(name,name_rect)

def draw_logos(x, y):
    
    # imdb logo
    imdb_bg = pygame.rect.Rect(0, 0, imdb_logo.get_width() + 4, imdb_logo.get_height() + 2)
    rect = imdb_logo.get_rect()
    imdb_bg.x = x
    imdb_bg.y = y
    rect.center = imdb_bg.center
    rect.y = rect.y + 2

    # yts logo 
    
    yts_rect = yts_logo.get_rect()
    yts_rect.x = imdb_bg.x + imdb_bg.width + 8
    yts_rect.y = imdb_bg.y
    yts_bg = pygame.rect.Rect(yts_rect.x, yts_rect.y, yts_rect.width, yts_rect.height)
    pygame.draw.rect(screen,backGroundCol,yts_bg)

    global prev_mouse_pressed
    if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()) and not prev_mouse_pressed:
        open_url_in_browser(film_info['imdb_link'])
        prev_mouse_pressed = True
    elif pygame.mouse.get_pressed()[0] and yts_rect.collidepoint(pygame.mouse.get_pos()) and not prev_mouse_pressed:
        open_url_in_browser(film_info['yts_link'])
        prev_mouse_pressed = True
    elif not pygame.mouse.get_pressed()[0]:
        prev_mouse_pressed = False

    screen.blit(yts_logo,yts_rect)
    pygame.draw.rect(screen, "#f6c800", imdb_bg, border_radius=2)
    screen.blit(imdb_logo, rect)
    

def display_text_animation(string,x,y):
    text = ''
    next_width = 0
    for i in range(len(string)):
        text += string[i]
        if string[i] == ' ' and next_width == 0:
            pass
        try:
            if string[i] == ' ' and i < len(string):
                next_width = textSur_font.render(text + string[i + 1:string.find(" ", i + 1) if string.find(" ", i + 1) != -1 else len(string)] + 'DU', True, "#FFFFFF").get_width()
            
        except:
            pass

        if (next_width > SCREEN_WIDTH +100 ):
            text += "\n"
            next_width = 0
        text_surface = desc_font.render(text, True, desc_color, backGroundCol)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        screen.blit(text_surface, text_rect)
        
        pygame.display.update()
        pygame.time.wait(5)

def draw_info(py_image,x,y):
    border = pygame.rect.Rect(0,0,py_image.get_width() + 10,py_image.get_height() + 10)
    rect = py_image.get_rect() 
    rect.x = x
    rect.y = y
    border.center = rect.center
    pygame.draw.rect(screen,"#000000",border,border_radius=3)
    screen.blit(py_image,rect)
    
    draw_logos(border.x + 3 , border.y + border.height + 7)

    current_y = border.y + 4 
    current_x = border.x + border.width + 7
    draw_text("Director","#FFFFFF",current_x ,current_y,"#FFFFFF",textSur_font,backGroundCol,0,0)
    temp_x = current_x + 1
    temp_y = current_y
    for director in film_info['director']:
        temp_x, temp_y = draw_text(director,"#FFFFFF",temp_x,temp_y + 34,'#000000',smallFont,True,current_x +1,current_y,"#000000")
        current_y = temp_y

    current_y = temp_y + 80
    current_x = border.x + border.width + 10
    draw_text("Genres","#FFFFFF",current_x ,current_y,"#FFFFFF",textSur_font,backGroundCol,current_x,current_y)

    temp_x = current_x + 1
    temp_y = current_y
    for genre in film_info['genres']:
        temp_x, temp_y = draw_text(genre,"#FFFFFF",temp_x,temp_y + 34,'#000000',smallFont,True,current_x +1,current_y,"#000000")
        current_y = temp_y 


    current_y = temp_y + 80
    current_x = border.x + border.width + 10
    draw_text("Cast","#FFFFFF",current_x ,current_y,"#FFFFFF",textSur_font,backGroundCol,current_x,current_y)

    temp_x = current_x + 1
    temp_y = current_y
    for actor in film_info['actors']:
        temp_x, temp_y = draw_text(actor,"#FFFFFF",temp_x,temp_y + 34,'#000000',smallFont,True,current_x +1,current_y,"#000000")
        current_y = temp_y

    current_y = temp_y + 100
    current_x = border.x + border.width + 10
    screen.blit(star,(current_x,current_y))
    raiting = film_info['rating']
    raiting_value = raiting[0]
    raiting_count = raiting[1]
    raiting_value = rating_font.render(str(raiting_value),True,'#FFFFFF',backGroundCol)
    raiting_value_rect = raiting_value.get_rect()
    raiting_value_rect.x = current_x + star.get_width() + 7
    raiting_value_rect.y = current_y
    screen.blit(raiting_value,raiting_value_rect)
    temp = rating_font.render("/5",True,'#787b7f',backGroundCol)
    temp_rect = raiting_value.get_rect()
    temp_rect.x = raiting_value_rect.x + raiting_value_rect.width
    temp_rect.y = current_y
    screen.blit(temp,temp_rect)
    raiting_count = rating_font.render(str(int(raiting_count / 1000)) + 'K',True,'#787b7f',backGroundCol)
    raiting_count_rect = raiting_count.get_rect()
    raiting_count_rect.x = raiting_value_rect.x 
    raiting_count_rect.y = raiting_value_rect.y + raiting_value_rect.width - 7
    screen.blit(raiting_count,raiting_count_rect)



manager = pygame_gui.UIManager(
    (SCREEN_WIDTH, SCREEN_HIGHT),theme_path="./theme.json",
    enable_live_theme_updates=True,
)

text_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((20, 50), (200, 40)),
    object_id="#main_text_entry",
    manager=manager,
    placeholder_text="username"

)

clock = pygame.time.Clock()

button1 = Button(
    "Get Movie", BUTTON_WIDTH, BUTTON_HIGHT, (SCREEN_WIDTH - BUTTON_WIDTH - 20, 50), 5
)
screen.fill(backGroundCol)

def kill_thread(thread_name):
    for thread in threading.enumerate():
        if thread.name == thread_name:
            thread.join()
            break

while True:
    UI_REFRESH_RATE = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if button1.pressed and text_input.text:
            try:
                button1.pressed = False
                kill_thread("thread_desc")
                screen.fill(backGroundCol)
                rand_film = get_random_film(text_input.text)
                
                film_info = rand_film.get_info()
                thread = threading.Thread(name = "thread_desc", target=display_text_animation,args=(film_info['description'].upper(),10,610)) 
                thread.start()
            except Exception as e:
                print(e)
        
        manager.process_events(event)

    manager.update(UI_REFRESH_RATE)
    manager.draw_ui(screen)
    button1.draw()
    if film_info:
        draw_movie_name(film_info['film_name'],150)
        draw_info(film_info['poster'],20,210)

    pygame.display.update()
    clock.tick(40)
