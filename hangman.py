import pygame   # Bibliothèque principale pour créer des jeux 2D
import random   # Module pour générer des valeurs aléatoires
import math     # Module pour les fonctions mathématiques (sin, cos, pi, etc.)
import sys      # Module système pour quitter proprement l'application
from datetime import datetime  # Module pour gérer les dates/heures (non utilisé ici)
import os       # Module pour interagir avec le système de fichiers

# === INITIALISATION DE PYGAME ===
pygame.init()        # Initialise tous les modules pygame
pygame.mixer.init()  # Initialise spécifiquement le module audio de pygame

# === CONSTANTES GLOBALES ===
# Dimensions de la fenêtre de jeu
WINDOW_WIDTH = 1000   # Largeur en pixels
WINDOW_HEIGHT = 700   # Hauteur en pixels
FPS = 60             # Images par seconde (fluidité du jeu)

# === PALETTE DE COULEURS MODERNES ===
# Couleurs définies en format RGB (Rouge, Vert, Bleu) de 0 à 255
DARK_BLUE = (25, 42, 86)      # Bleu foncé pour les fonds
LIGHT_BLUE = (59, 130, 246)   # Bleu clair pour les accents
PURPLE = (139, 69, 199)       # Violet pour la variété colorée
PINK = (236, 72, 153)         # Rose pour les effets festifs
YELLOW = (250, 204, 21)       # Jaune pour les succès et alertes
GREEN = (34, 197, 94)         # Vert pour les bonnes réponses
RED = (239, 68, 68)           # Rouge pour les erreurs
WHITE = (255, 255, 255)       # Blanc pur
BLACK = (0, 0, 0)             # Noir pur
GRAY = (156, 163, 175)        # Gris moyen pour les éléments neutres
DARK_GRAY = (75, 85, 99)      # Gris foncé pour les ombres

# Couleurs pour le dégradé d'arrière-plan
GRADIENT_START = (30, 41, 59)  # Couleur du haut du dégradé
GRADIENT_END = (15, 23, 42)    # Couleur du bas du dégradé

class FallingLetter:
    """
    Classe qui gère les lettres qui tombent en arrière-plan
    Crée un effet visuel dynamique avec traînée et particules
    """
    
    def __init__(self):
        """
        Constructeur qui initialise une lettre tombante avec des propriétés aléatoires
        """
        # === POSITION ET MOUVEMENT ===
        self.x = random.randint(0, WINDOW_WIDTH)     # Position X aléatoire sur la largeur
        self.y = random.randint(-200, -50)           # Position Y au-dessus de l'écran
        
        # === PROPRIÉTÉS VISUELLES ===
        self.letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # Lettre aléatoire
        # Couleur aléatoire parmi les couleurs vives
        self.color = random.choice([LIGHT_BLUE, PURPLE, PINK, GREEN, YELLOW, WHITE])
        self.speed = random.uniform(1, 4)            # Vitesse de chute variable
        self.size = random.randint(32, 64)           # Taille de police variable
        self.alpha = random.randint(200, 255)        # Transparence (presque opaque)
        
        # === ROTATION ===
        self.rotation = random.uniform(0, 360)       # Angle de rotation initial
        self.rotation_speed = random.uniform(-2, 2)  # Vitesse de rotation (peut être négative)
        
        # === EFFET DE TRAÎNÉE ===
        self.trail_positions = []      # Liste des positions précédentes pour la traînée
        self.trail_max_length = 5      # Longueur maximum de la traînée
        
        # === PARTICULES D'ACCOMPAGNEMENT ===
        self.particles = []            # Liste des petites particules autour de la lettre
        self.particle_timer = 0        # Compteur pour créer des particules périodiquement
    
    def update(self):
        """
        Met à jour la position et l'état de la lettre à chaque frame
        """
        # === GESTION DE LA TRAÎNÉE ===
        # Sauvegarde la position actuelle avec sa transparence pour l'effet de traînée
        self.trail_positions.append((self.x, self.y, self.alpha))
        
        # Limite la longueur de la traînée en supprimant les anciennes positions
        if len(self.trail_positions) > self.trail_max_length:
            self.trail_positions.pop(0)  # Supprime le premier élément (plus ancien)
        
        # === MOUVEMENT DE LA LETTRE ===
        self.y += self.speed                    # Déplace vers le bas selon la vitesse
        self.rotation += self.rotation_speed    # Fait tourner la lettre
        
        # === CRÉATION DE PARTICULES PÉRIODIQUES ===
        self.particle_timer += 1  # Incrémente le compteur
        
        # Crée des particules à intervalles aléatoires
        if self.particle_timer > random.randint(10, 30):
            self.particle_timer = 0  # Remet le compteur à zéro
            
            # Ajoute 2 petites particules autour de la lettre
            for _ in range(2):
                # Position légèrement décalée de la lettre principale
                particle_x = self.x + random.randint(-10, 10)
                particle_y = self.y + random.randint(-5, 5)
                particle_color = self.color  # Même couleur que la lettre
                particle_speed = random.uniform(0.5, 1.5)    # Vitesse plus lente
                particle_alpha = random.randint(50, 120)     # Plus transparente
                
                # Stocke les propriétés de la particule dans un dictionnaire
                self.particles.append({
                    'x': particle_x,
                    'y': particle_y,
                    'color': particle_color,
                    'speed': particle_speed,
                    'alpha': particle_alpha,
                    'life': random.randint(30, 60)  # Durée de vie en frames
                })
        
        # === MISE À JOUR DES PARTICULES ===
        # Utilise une copie de la liste pour pouvoir modifier l'originale pendant l'itération
        for particle in self.particles[:]:
            particle['y'] += particle['speed']  # Déplace la particule vers le bas
            particle['alpha'] -= 2              # Réduit la transparence
            particle['life'] -= 1               # Réduit la durée de vie
            
            # Supprime la particule si elle est "morte" ou invisible
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.particles.remove(particle)
        
        # === RÉAPPARITION EN HAUT ===
        # Si la lettre est sortie de l'écran par le bas
        if self.y > WINDOW_HEIGHT + 100:
            # Remet la lettre en haut avec de nouvelles propriétés aléatoires
            self.y = random.randint(-200, -50)
            self.x = random.randint(0, WINDOW_WIDTH)
            self.letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            self.color = random.choice([LIGHT_BLUE, PURPLE, PINK, GREEN, YELLOW, WHITE])
            self.speed = random.uniform(1, 4)
            self.size = random.randint(32, 64)
            self.alpha = random.randint(200, 255)
            # Remet à zéro les effets visuels
            self.trail_positions.clear()
            self.particles.clear()
    
    def draw(self, screen, font):
        """
        Dessine la lettre avec tous ses effets visuels
        
        Args:
            screen: surface pygame où dessiner
            font: police à utiliser pour le rendu du texte
        """
        # === DESSIN DE LA TRAÎNÉE ===
        # Parcourt toutes les positions de la traînée sauf la dernière (position actuelle)
        for i, (trail_x, trail_y, trail_alpha) in enumerate(self.trail_positions):
            if i < len(self.trail_positions) - 1:  # Pas la position actuelle
                # Calcule la transparence dégradée selon la position dans la traînée
                fade_alpha = int(trail_alpha * (i / len(self.trail_positions)) * 0.3)
                
                if fade_alpha > 10:  # Seulement si suffisamment visible
                    # Crée le texte de la traînée
                    trail_text = font.render(self.letter, True, self.color)
                    # Applique la rotation
                    trail_rotated = pygame.transform.rotate(trail_text, self.rotation)
                    
                    # Crée une surface temporaire avec transparence
                    temp_trail = pygame.Surface(trail_rotated.get_size(), pygame.SRCALPHA)
                    temp_trail.set_alpha(fade_alpha)  # Applique la transparence
                    temp_trail.blit(trail_rotated, (0, 0))
                    
                    # Centre et dessine la traînée
                    trail_rect = temp_trail.get_rect()
                    trail_rect.center = (trail_x, trail_y)
                    screen.blit(temp_trail, trail_rect)
        
        # === DESSIN DES PARTICULES D'ACCOMPAGNEMENT ===
        for particle in self.particles:
            if particle['alpha'] > 0:  # Seulement si visible
                # Crée une petite surface pour la particule
                particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                # Dessine un petit cercle coloré avec transparence
                color_with_alpha = (*particle['color'], particle['alpha'])
                pygame.draw.circle(particle_surf, color_with_alpha, (2, 2), 2)
                # Positionne et dessine la particule
                screen.blit(particle_surf, (particle['x'] - 2, particle['y'] - 2))
        
        # === DESSIN DE LA LETTRE PRINCIPALE ===
        # Crée le texte de la lettre avec sa couleur
        letter_text = font.render(self.letter, True, self.color)
        
        # Applique la rotation à la lettre
        rotated_letter = pygame.transform.rotate(letter_text, self.rotation)
        
        # Crée une surface temporaire pour appliquer la transparence
        temp_surface = pygame.Surface(rotated_letter.get_size(), pygame.SRCALPHA)
        temp_surface.set_alpha(self.alpha)  # Applique la transparence
        temp_surface.blit(rotated_letter, (0, 0))
        
        # Centre la lettre sur sa position et la dessine
        letter_rect = temp_surface.get_rect()
        letter_rect.center = (self.x, self.y)
        screen.blit(temp_surface, letter_rect)

class Particle:
    """
    Classe pour créer des particules d'effets visuels (explosions, succès, etc.)
    """
    def __init__(self, x, y, color, velocity):
        """
        Constructeur de la particule d'effet
        
        Args:
            x, y: position initiale
            color: couleur RGB de la particule
            velocity: tuple (vx, vy) pour la vitesse de déplacement
        """
        self.x = x                          # Position horizontale
        self.y = y                          # Position verticale
        self.color = color                  # Couleur RGB
        self.velocity = velocity            # Vitesse de déplacement (vx, vy)
        self.life = 255                     # Durée de vie (255 = opaque, 0 = invisible)
        self.size = random.uniform(2, 5)    # Taille aléatoire de la particule
    
    def update(self):
        """
        Met à jour la position et l'état de la particule
        """
        self.x += self.velocity[0]  # Déplace selon la vitesse X
        self.y += self.velocity[1]  # Déplace selon la vitesse Y
        self.life -= 3              # Réduit la durée de vie (disparition progressive)
        self.size *= 0.99           # Réduit légèrement la taille
    
    def draw(self, screen):
        """
        Dessine la particule si elle est encore visible
        """
        if self.life > 0:  # Vérifie si la particule est encore vivante
            alpha = max(0, self.life)  # Calcule la transparence
            color = (*self.color, alpha)  # Ajoute la transparence à la couleur
            
            # Crée une surface temporaire avec transparence
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            # Dessine un cercle coloré
            pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
            # Positionne et dessine la particule
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class Button:
    """
    Classe pour créer des boutons interactifs avec animations
    """
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        """
        Constructeur du bouton
        """
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle de collision
        self.text = text                               # Texte du bouton
        self.color = color                            # Couleur de fond
        self.text_color = text_color                  # Couleur du texte
        # Couleur plus claire pour l'effet de survol
        self.hover_color = tuple(min(255, c + 30) for c in color)
        self.is_hovered = False                       # État de survol
        self.scale = 1.0                             # Échelle pour l'animation
        
    def handle_event(self, event):
        """
        Gère les événements de clic sur le bouton
        Retourne True si le bouton a été cliqué
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def update(self, mouse_pos):
        """
        Met à jour l'état du bouton selon la position de la souris
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        target_scale = 1.05 if self.is_hovered else 1.0
        # Animation douce d'échelle (interpolation)
        self.scale += (target_scale - self.scale) * 0.1
    
    def draw(self, screen, font):
        """
        Dessine le bouton avec ses effets visuels
        """
        # Dessine l'ombre (décalée)
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Choisit la couleur selon l'état de survol
        color = self.hover_color if self.is_hovered else self.color
        
        # Calcule la taille avec l'effet d'échelle
        scaled_rect = self.rect.copy()
        scale_offset = (self.scale - 1) * 10
        scaled_rect.inflate_ip(scale_offset, scale_offset)
        
        # Dessine le bouton avec coins arrondis
        pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, scaled_rect, 2, border_radius=10)
        
        # Dessine le texte centré
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)

def draw_gradient_background(screen):
    """
    Dessine un fond dégradé vertical sur tout l'écran
    Crée une transition douce entre deux couleurs
    """
    for y in range(WINDOW_HEIGHT):  # Pour chaque ligne de pixels
        ratio = y / WINDOW_HEIGHT   # Ratio de progression (0 en haut, 1 en bas)
        
        # Interpolation linéaire entre les couleurs de début et de fin
        r = int(GRADIENT_START[0] * (1 - ratio) + GRADIENT_END[0] * ratio)
        g = int(GRADIENT_START[1] * (1 - ratio) + GRADIENT_END[1] * ratio)
        b = int(GRADIENT_START[2] * (1 - ratio) + GRADIENT_END[2] * ratio)
        
        # Dessine une ligne horizontale avec cette couleur
        pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

def draw_animated_stickman(screen, penalties, animation_time):
    """
    Dessine le bonhomme pendu avec des animations selon le nombre d'erreurs
    
    Args:
        screen: surface où dessiner
        penalties: nombre d'erreurs (détermine les parties visibles)
        animation_time: temps pour les animations de balancement
    """
    x, y = 200, 300  # Position de base de la potence
    
    # === ANIMATION DE BALANCEMENT ===
    # Utilise une fonction sinusoïdale pour créer un mouvement de balancement
    sway = math.sin(animation_time * 0.05) * 2  # Amplitude de 2 pixels
    
    # === DESSIN PROGRESSIF DE LA POTENCE ===
    if penalties >= 1:  # Base de la potence
        # Ombre de la base (plus foncée)
        pygame.draw.rect(screen, DARK_GRAY, (x-60, y+155, 120, 10))
        # Base principale (plus claire)
        pygame.draw.rect(screen, GRAY, (x-55, y+150, 110, 10))
    
    if penalties >= 2:  # Poteau vertical
        # Rectangle brun pour le poteau
        pygame.draw.rect(screen, (139, 69, 19), (x-35, y-60, 10, 210))
        
    if penalties >= 3:  # Poteau horizontal
        # Traverse horizontale de la potence
        pygame.draw.rect(screen, (139, 69, 19), (x-35, y-60, 65, 8))
        
    if penalties >= 4:  # Corde animée
        rope_color = (101, 67, 33)  # Couleur marron foncé
        # Dessine la corde comme une série de petits cercles
        for i in range(0, 30, 3):  # De 0 à 30 par pas de 3
            rope_y = y - 50 + i + sway * 0.3  # Position avec léger balancement
            pygame.draw.circle(screen, rope_color, (x+30, int(rope_y)), 2)
    
    # === POSITION DU BONHOMME AVEC BALANCEMENT ===
    man_x = x + 30 + sway  # Position X avec effet de balancement
    man_y = y - 20         # Position Y fixe
    
    if penalties >= 5:  # Tête avec visage
        # Ombre de la tête pour l'effet de profondeur
        pygame.draw.circle(screen, (0, 0, 0, 100), (int(man_x + 2), int(man_y + 2)), 22)
        # Tête couleur chair
        pygame.draw.circle(screen, (255, 220, 177), (int(man_x), int(man_y)), 20)
        # Contour noir de la tête
        pygame.draw.circle(screen, BLACK, (int(man_x), int(man_y)), 20, 3)
        
        # === EXPRESSION DU VISAGE ===
        if penalties >= 8:  # Visage de mort (yeux en X)
            # Œil gauche en X rouge
            pygame.draw.line(screen, RED, (int(man_x - 8), int(man_y - 5)), (int(man_x - 4), int(man_y - 1)), 2)
            pygame.draw.line(screen, RED, (int(man_x - 4), int(man_y - 5)), (int(man_x - 8), int(man_y - 1)), 2)
            # Œil droit en X rouge
            pygame.draw.line(screen, RED, (int(man_x + 4), int(man_y - 5)), (int(man_x + 8), int(man_y - 1)), 2)
            pygame.draw.line(screen, RED, (int(man_x + 8), int(man_y - 5)), (int(man_x + 4), int(man_y - 1)), 2)
            # Bouche triste (arc vers le bas)
            pygame.draw.arc(screen, RED, (int(man_x - 8), int(man_y + 8), 16, 8), math.pi, 2 * math.pi, 2)
        else:  # Visage normal
            # Yeux normaux (petits cercles noirs)
            pygame.draw.circle(screen, BLACK, (int(man_x - 6), int(man_y - 3)), 2)
            pygame.draw.circle(screen, BLACK, (int(man_x + 6), int(man_y - 3)), 2)
    
    if penalties >= 6:  # Corps
        # Ligne verticale pour le corps
        pygame.draw.line(screen, BLACK, (int(man_x), int(man_y + 20)), (int(man_x), int(man_y + 80)), 4)
    
    if penalties >= 7:  # Bras gauche animé
        # Position du bras avec animation sinusoïdale
        arm_end_x = man_x - 25 + math.sin(animation_time * 0.1) * 3
        pygame.draw.line(screen, BLACK, (int(man_x), int(man_y + 40)), (int(arm_end_x), int(man_y + 55)), 4)
    
    if penalties >= 8:  # Bras droit animé
        # Animation déphasée (+ pi) pour un mouvement alterné
        arm_end_x = man_x + 25 + math.sin(animation_time * 0.1 + math.pi) * 3
        pygame.draw.line(screen, BLACK, (int(man_x), int(man_y + 40)), (int(arm_end_x), int(man_y + 55)), 4)
    
    if penalties >= 9:  # Jambe gauche
        pygame.draw.line(screen, BLACK, (int(man_x), int(man_y + 80)), (int(man_x - 20), int(man_y + 110)), 4)
    
    if penalties >= 10:  # Jambe droite (mort complète)
        pygame.draw.line(screen, BLACK, (int(man_x), int(man_y + 80)), (int(man_x + 20), int(man_y + 110)), 4)

def draw_word_display(screen, word, guessed_letters, font, animation_time):
    """
    Affiche le mot à deviner avec des animations colorées
    Les lettres trouvées rebondissent, les autres sont des tirets animés
    
    Args:
        screen: surface où dessiner
        word: mot à deviner
        guessed_letters: set des lettres déjà trouvées
        font: police pour le rendu
        animation_time: temps pour les animations
    """
    # Calcule la position de départ pour centrer le mot
    x_start = WINDOW_WIDTH // 2 - (len(word) * 40) // 2
    y_pos = 500
    
    for i, letter in enumerate(word):  # Pour chaque lettre du mot
        x = x_start + i * 50  # Position X (50 pixels d'espacement)
        
        if letter in guessed_letters:  # Si la lettre a été devinée
            # === ANIMATION DE REBOND ===
            # Chaque lettre a son propre déphasage (i * 0.5) pour un effet de vague
            bounce = math.sin(animation_time * 0.1 + i * 0.5) * 3
            
            # === EFFET D'OMBRE ===
            shadow_surf = font.render(letter, True, (0, 0, 0, 100))
            screen.blit(shadow_surf, (x + 2, y_pos + 2 + bounce))
            
            # === LETTRE COLORÉE ===
            # Choisit une couleur selon la position de la lettre (cycle de 5 couleurs)
            color = [LIGHT_BLUE, PURPLE, PINK, GREEN, YELLOW][i % 5]
            letter_surf = font.render(letter, True, color)
            screen.blit(letter_surf, (x, y_pos + bounce))
        else:  # Si la lettre n'a pas été devinée
            # === TIRET ANIMÉ ===
            # Le tiret bouge légèrement avec une animation sinusoïdale
            underscore_y = y_pos + 40 + math.sin(animation_time * 0.08 + i * 0.3) * 2
            pygame.draw.line(screen, WHITE, (x, int(underscore_y)), (x + 30, int(underscore_y)), 4)

class HangmanDeluxe:
    """
    Classe principale qui gère tout le jeu du pendu avancé
    Inclut : base de mots étendue, sons, particules, lettres tombantes, options
    """
    
    def __init__(self):
        """
        Constructeur qui initialise tout le système de jeu
        """
        # === INITIALISATION DE LA BASE DE DONNÉES ===
        self.init_word_database()  # Charge tous les mots français
        
        # === CRÉATION DES POLICES ===
        self.big_font = pygame.font.Font(None, 72)      # Grande police pour les titres
        self.medium_font = pygame.font.Font(None, 48)   # Police moyenne pour le mot
        self.small_font = pygame.font.Font(None, 36)    # Petite police pour les infos
        
        # === VARIABLES D'ÉTAT DU JEU ===
        self.particles = []          # Liste des particules d'effets
        self.animation_time = 0      # Compteur global pour toutes les animations
        self.music_volume = 0.3      # Volume de la musique (0.0 à 1.0)
        self.sound_enabled = True    # État du son (activé/désactivé)
        self.show_options = False    # Affichage du panneau d'options
        
        # === SYSTÈME DE LETTRES TOMBANTES ===
        self.falling_letters = []                    # Liste des lettres d'arrière-plan
        self.letter_font = pygame.font.Font(None, 48)  # Police pour les lettres tombantes
        
        # Crée 25 lettres tombantes pour un effet dense
        for _ in range(25):
            self.falling_letters.append(FallingLetter())
        
        # === INITIALISATION DES SYSTÈMES ===
        self.init_audio()    # Configure le système audio
        self.reset_game()    # Démarre une nouvelle partie
    
    def init_word_database(self):
        """
        Initialise une base de données étendue de mots français
        Organisée par catégories pour plus de variété
        """
        print("Chargement de la base de mots française étendue...")
        
        # === MOTS PAR CATÉGORIES ===
        # Dictionnaire avec des catégories thématiques
        self.word_categories = {
            "ANIMAUX": [
                "ELEPHANT", "GIRAFE", "KANGOUROU", "CROCODILE", "PAPILLON", "RHINOCEROS",
                "LEOPARD", "HIPPOPOTAME", "CHIMPANZE", "GORILLE", "ANTILOPE", "GAZELLE",
                "CHAMEAU", "DROMADAIRE", "ZEBRE", "AUTRUCHE", "FLAMANT", "PELICAN",
                "MANCHOT", "PINGOUIN", "PHOQUE", "BALEINE", "DAUPHIN", "REQUIN",
                "PIEUVRE", "MEDUSE", "HOMARD", "CRABE", "TORTUE", "SERPENT",
                "LEZARD", "GRENOUILLE", "SALAMANDRE", "LIBELLULE", "COCCINELLE",
                "ESCARGOT", "ARAIGNEE", "FOURMI", "ABEILLE", "GUEPE", "MOUCHE",
                "MOUSTIQUE", "CHENILLE", "SCARABEE", "SAUTERELLE"
            ],
            "PAYS": [
                "FRANCE", "ESPAGNE", "ITALIE", "ALLEMAGNE", "PORTUGAL", "GRECE",
                "NORVEGE", "SUEDE", "DANEMARK", "FINLANDE", "ISLANDE", "IRLANDE",
                "ECOSSE", "ANGLETERRE", "BELGIQUE", "SUISSE", "AUTRICHE",
                "POLOGNE", "HONGRIE", "ROUMANIE", "BULGARIE", "CROATIE",
                "JAPON", "CHINE", "COREE", "THAILANDE", "VIETNAM", "CAMBODGE",
                "INDE", "PAKISTAN", "BANGLADESH", "NEPAL", "BHOUTAN",
                "AUSTRALIE", "FIDJI", "VANUATU", "SAMOA", "TONGA",
                "CANADA", "MEXIQUE", "GUATEMALA", "COSTA-RICA", "PANAMA",
                "BRESIL", "ARGENTINE", "CHILI", "PEROU", "COLOMBIE", "VENEZUELA",
                "EGYPTE", "MAROC", "ALGERIE", "TUNISIE", "LIBYE", "SOUDAN",
                "KENYA", "TANZANIE", "OUGANDA", "RWANDA", "ETHIOPIE", "GHANA",
                "RUSSIE", "UKRAINE", "BELARUS", "LITUANIE", "LETTONIE", "ESTONIE"
            ],
            "NOURRITURE": [
                "BAGUETTE", "CROISSANT", "BRIOCHE", "PAIN", "FROMAGE", "CAMEMBERT",
                "ROQUEFORT", "GRUYERE", "EMMENTAL", "BRIE", "CHEVRE", "YAOURT",
                "CREPE", "GAUFFRE", "MACARON", "ECLAIR", "PROFITEROLE", "MADELEINE",
                "RATATOUILLE", "BOUILLABAISSE", "CASSOULET", "COUSCOUS", "PAELLA",
                "PIZZA", "LASAGNE", "SPAGHETTI", "RAVIOLI", "GNOCCHI", "RISOTTO",
                "SUSHI", "SASHIMI", "TEMPURA", "RAMEN", "YAKITORI", "MISO",
                "HAMBURGER", "SANDWICH", "SALADE", "SOUPE", "POTAGE", "VELOUTE",
                "POMME", "POIRE", "BANANE", "ORANGE", "CITRON", "PAMPLEMOUSSE",
                "FRAISE", "FRAMBOISE", "MYRTILLE", "CASSIS", "GROSEILLE", "CERISE",
                "PECHE", "ABRICOT", "PRUNE", "RAISIN", "MELON", "PASTEQUE",
                "ANANAS", "MANGUE", "KIWI", "PASSION", "LITCHI", "PAPAYE",
                "CHOCOLAT", "BONBON", "CARAMEL", "NOUGAT", "PRALINE", "TRUFFE"
            ],
            "METIERS": [
                "MEDECIN", "INFIRMIERE", "CHIRURGIEN", "DENTISTE", "PHARMACIEN",
                "VETERINAIRE", "PROFESSEUR", "INSTITUTEUR", "DIRECTEUR", "SECRETAIRE",
                "AVOCAT", "JUGE", "NOTAIRE", "HUISSIER", "COMMISSAIRE", "POLICIER",
                "POMPIER", "AMBULANCIER", "PILOTE", "STEWARD", "CAPITAINE", "MARIN",
                "CUISINIER", "SERVEUR", "BARMAN", "PATISSIER", "BOULANGER", "BOUCHER",
                "POISSONNIER", "EPICIER", "CAISSIER", "VENDEUR", "COMMERCIAL", "BANQUIER",
                "COMPTABLE", "ECONOMISTE", "INGENIEUR", "ARCHITECTE", "DESIGNER", "ARTISTE",
                "PEINTRE", "SCULPTEUR", "MUSICIEN", "CHANTEUR", "DANSEUR", "ACTEUR",
                "JOURNALISTE", "PHOTOGRAPHE", "CAMERAMAN", "MONTEUR", "REALISATEUR",
                "ELECTRICIEN", "PLOMBIER", "MENUISIER", "MAÇON", "COUVREUR", "JARDINIER"
            ],
            "OBJETS": [
                "ORDINATEUR", "TELEPHONE", "TABLETTE", "CLAVIER", "SOURIS", "ECRAN",
                "IMPRIMANTE", "SCANNER", "APPAREIL-PHOTO", "CAMERA", "TELEVISION",
                "REFRIGERATEUR", "LAVE-LINGE", "LAVE-VAISSELLE", "ASPIRATEUR", "MICRO-ONDE",
                "VOITURE", "BICYCLETTE", "MOTOCYCLETTE", "AUTOBUS", "TRAMWAY", "METRO",
                "AVION", "HELICOPTERE", "BATEAU", "YACHT", "SOUS-MARIN", "FUSEE",
                "MONTRE", "COLLIER", "BRACELET", "BAGUE", "BOUCLES-OREILLES", "LUNETTES",
                "PARAPLUIE", "SAC", "VALISE", "PORTEFEUILLE", "CLES", "TELEPHONE",
                "LIVRE", "MAGAZINE", "JOURNAL", "CAHIER", "STYLO", "CRAYON",
                "GOMME", "REGLE", "CALCULATRICE", "DICTIONNAIRE", "ATLAS", "CARTE",
                "CHAISE", "TABLE", "ARMOIRE", "COMMODE", "ETAGERE", "BIBLIOTHEQUE",
                "LAMPE", "MIROIR", "RIDEAU", "TAPIS", "COUSSIN", "COUVERTURE"
            ],
            "SPORTS": [
                "FOOTBALL", "BASKETBALL", "VOLLEYBALL", "HANDBALL", "RUGBY", "TENNIS",
                "BADMINTON", "PING-PONG", "SQUASH", "GOLF", "BASEBALL", "CRICKET",
                "NATATION", "PLONGEE", "SURF", "VOILE", "AVIRON", "CANOE",
                "CYCLISME", "COURSE", "MARATHON", "TRIATHLON", "ATHLETISME", "SAUT",
                "LANCER", "MUSCULATION", "BOXE", "KARATE", "JUDO", "TAEKWONDO",
                "ESCRIME", "ARCHERIE", "TIR", "EQUITATION", "POLO", "DRESSAGE",
                "SKI", "SNOWBOARD", "PATINAGE", "HOCKEY", "LUGE", "BOBSLEIGH",
                "ESCALADE", "ALPINISME", "RANDONNEE", "CAMPING", "PECHE", "CHASSE",
                "PARAPENTE", "DELTAPLANE", "PARACHUTISME", "BUNGEE", "RAFTING"
            ],
            "SCIENCE": [
                "PHYSIQUE", "CHIMIE", "BIOLOGIE", "MATHEMATIQUES", "ASTRONOMIE",
                "GEOLOGIE", "METEOROLOGIE", "OCEANOGRAPHIE", "BOTANIQUE", "ZOOLOGIE",
                "ANATOMIE", "PHYSIOLOGIE", "GENETIQUE", "EVOLUTION", "ECOLOGIE",
                "MOLECULE", "ATOME", "ELECTRON", "PROTON", "NEUTRON", "PHOTON",
                "TELESCOPE", "MICROSCOPE", "LABORATOIRE", "EXPERIENCE", "HYPOTHESE",
                "PLANETE", "ETOILE", "GALAXIE", "COMETE", "ASTEROIDE", "METEORITE",
                "VOLCAN", "SEISME", "TSUNAMI", "OURAGAN", "TORNADE", "CYCLONE"
            ],
            "MUSIQUE": [
                "PIANO", "GUITARE", "VIOLON", "VIOLONCELLE", "CONTREBASSE", "HARPE",
                "FLUTE", "CLARINETTE", "SAXOPHONE", "TROMPETTE", "TROMBONE", "TUBA",
                "BATTERIE", "TAMBOUR", "CYMBALE", "TRIANGLE", "XYLOPHONE", "ACCORDEON",
                "HARMONICA", "BANJO", "MANDOLINE", "UKULELE", "SYNTHESISEUR", "ORGUE",
                "CONCERT", "ORCHESTRA", "SYMPHONIE", "OPERA", "CHORALE", "MELODIE",
                "RYTHME", "HARMONIE", "PARTITION", "PORTEE", "CLEF", "NOTE"
            ]
        }
        
        # === MOTS PAR NIVEAU DE DIFFICULTÉ ===
        # Séparation par difficulté croissante pour adapter le défi
        self.difficulty_words = {
            "FACILE": [
                "CHAT", "CHIEN", "MAISON", "VOITURE", "PAIN", "EAU", "FEU", "SOLEIL",
                "LUNE", "ETOILE", "FLEUR", "ARBRE", "OISEAU", "POISSON", "LIVRE",
                "TABLE", "CHAISE", "LIT", "PORTE", "FENETRE", "ROUGE", "BLEU",
                "VERT", "JAUNE", "NOIR", "BLANC", "GRAND", "PETIT", "JOUR", "NUIT",
                "MAIN", "PIED", "TETE", "COEUR", "YEUX", "NEZ", "BOUCHE", "OREILLE",
                "BRAS", "JAMBE", "DOS", "VENTRE", "CHEVEUX", "DENT", "ONGLE"
            ],
            "MOYEN": [
                "ORDINATEUR", "TELEPHONE", "REFRIGERATEUR", "TELEVISION", "PHARMACIE",
                "RESTAURANT", "UNIVERSITE", "BIBLIOTHEQUE", "HOPITAL", "AEROPORT",
                "PARAPLUIE", "CHOCOLAT", "SANDWICH", "PROGRAMME", "ALPHABET",
                "DICTIONNAIRE", "PROBLEME", "SOLUTION", "QUESTION", "REPONSE",
                "MONTAGNE", "RIVIERE", "OCEAN", "DESERT", "FORET", "PRAIRIE",
                "VILLAGE", "QUARTIER", "AVENUE", "BOULEVARD", "CARREFOUR", "PARKING"
            ],
            "DIFFICILE": [
                "EXTRATERRESTRE", "HIPPOPOTAME", "CHRYSANTHEME", "PSYCHOLOGIE",
                "PHILOSOPHIE", "ARCHITECTURE", "PHOTOGRAPHIE", "GEOGRAPHIE",
                "ORTHOGRAPHE", "SYNONYME", "ACRONYME", "PALINDROME", "ANAGRAMME",
                "ONOMATOPEE", "METAPHORE", "ALLEGORIE", "OXYMORON", "EUPHEMISME",
                "CACOPHONIE", "POLYPHONIE", "XENOPHOBIE", "CLAUSTROPHOBIE",
                "AGORAPHOBIE", "PHILANTHROPE", "MISANTHROPE", "HYPERBOLE"
            ]
        }
        
        # === STATISTIQUES DE LA BASE ===
        # Calcule et affiche le nombre total de mots disponibles
        total_words = sum(len(words) for words in self.word_categories.values())
        total_difficulty = sum(len(words) for words in self.difficulty_words.values())
        print(f"Base chargée: {total_words + total_difficulty} mots français !")
    
    def get_word_to_guess(self):
        """
        Sélectionne un mot à deviner selon une logique de probabilité
        70% par catégorie thématique, 30% par niveau de difficulté
        
        Returns:
            tuple: (mot_choisi, catégorie_ou_niveau)
        """
        if random.random() < 0.7:  # 70% de chance
            # Sélection par catégorie thématique
            category = random.choice(list(self.word_categories.keys()))
            word = random.choice(self.word_categories[category])
            return word, category
        else:  # 30% de chance
            # Sélection par niveau de difficulté
            difficulty = random.choice(list(self.difficulty_words.keys()))
            word = random.choice(self.difficulty_words[difficulty])
            return word, f"NIVEAU {difficulty}"
    
    def init_audio(self):
        """
        Initialise le système audio complet du jeu
        Charge la musique de fond et crée les effets sonores
        """
        try:
            # === CHARGEMENT DE LA MUSIQUE DE FOND ===
            # Chemin où chercher les fichiers audio
           # Chemin relatif vers le dossier assets (fonctionne peu importe où le script est lancé)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            music_path = os.path.join(script_dir, "assets", "musique_pendu.mp3")
            
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 = boucle infinie
                print(f"Musique chargée: {music_path}")
            else:
                print(f"Fichier audio non trouvé: {music_path}")
                self.create_fallback_music()  # Crée une musique de secours
            
            # Crée les effets sonores personnalisés
            self.create_sound_effects()
            
        except Exception as e:
            print(f"Erreur audio: {e}")
            # En cas d'erreur, utilise les solutions de secours
            self.create_fallback_music()
            self.create_sound_effects()
    
    def create_fallback_music(self):
        """
        Crée une musique de fond simple si aucun fichier n'est trouvé
        Génère un accord ambient relaxant mathématiquement
        """
        try:
            # === PARAMÈTRES DE GÉNÉRATION ===
            duration = 8.0        # Durée en secondes
            sample_rate = 22050   # Fréquence d'échantillonnage
            frames = int(duration * sample_rate)  # Nombre total d'échantillons
            
            music = []  # Liste pour stocker les échantillons audio
            
            # === GÉNÉRATION D'UN ACCORD AMBIENT ===
            for i in range(frames):
                time = float(i) / sample_rate  # Temps actuel en secondes
                
                # Fréquences d'un accord relaxant (La mineur avec extensions)
                freq1, freq2, freq3, freq4 = 220, 277, 330, 440  # Hz
                
                # Génère 4 oscillateurs avec des volumes différents
                osc1 = math.sin(2 * math.pi * freq1 * time) * 0.1   # Fondamentale
                osc2 = math.sin(2 * math.pi * freq2 * time) * 0.08  # Tierce
                osc3 = math.sin(2 * math.pi * freq3 * time) * 0.06  # Quinte
                osc4 = math.sin(2 * math.pi * freq4 * time) * 0.04  # Octave
                
                # Enveloppe de fade in/out pour éviter les clics
                fade = min(1.0, time * 4, (duration - time) * 4)
                
                # Combine tous les oscillateurs avec l'enveloppe
                wave = (osc1 + osc2 + osc3 + osc4) * fade
                
                # Convertit en format entier 16-bit
                music.append(int(wave * 32767))
            
            # Crée l'objet son pygame
            self.background_music = pygame.sndarray.make_sound(
                pygame.array.array('h', music))
            
            # Lance la musique en boucle
            if hasattr(self, 'background_music'):
                self.background_music.play(loops=-1)
                self.background_music.set_volume(self.music_volume)
                
        except Exception as e:
            print(f"Impossible de créer la musique de secours: {e}")
    
    def create_sound_effects(self):
        """
        Crée tous les effets sonores du jeu avec numpy
        Génère des sons synthétiques pour différents événements
        """
        try:
            import numpy as np  # Nécessaire pour la manipulation audio avancée
            print("Numpy importé avec succès")
            
            self.sounds = {}  # Dictionnaire pour stocker tous les sons
            
            # === PARAMÈTRES COMMUNS ===
            duration = 0.3        # Durée standard des effets
            sample_rate = 22050   # Fréquence d'échantillonnage
            frames = int(duration * sample_rate)
            print(f"Création de sons avec {frames} frames à {sample_rate}Hz")
            
            # === SON DE VICTOIRE (mélodie joyeuse ascendante) ===
            victory_sound = []
            for i in range(frames):
                time = float(i) / sample_rate
                # Mélodie ascendante avec harmoniques
                freq1 = 523 + (i / frames) * 200  # Do à Sol (montée)
                freq2 = 659 + (i / frames) * 150  # Mi à Si (harmonie)
                
                # Combine les deux fréquences
                wave1 = math.sin(2 * math.pi * freq1 * time) * 0.3
                wave2 = math.sin(2 * math.pi * freq2 * time) * 0.2
                
                # Convertit en stéréo (même son sur les 2 canaux)
                sample = int((wave1 + wave2) * 32767)
                victory_sound.append([sample, sample])
            
            # Convertit en tableau numpy stéréo et crée le son
            victory_array = np.array(victory_sound, dtype=np.int16)
            self.sounds['victory'] = pygame.sndarray.make_sound(victory_array)
            print("Son de victoire créé")
            
            # === SON D'ERREUR (note descendante désagréable) ===
            error_sound = []
            for i in range(frames):
                time = float(i) / sample_rate
                freq = 400 - (i / frames) * 200  # Descend de 400Hz à 200Hz
                wave = math.sin(2 * math.pi * freq * time) * 0.3
                
                # Ajoute une distorsion pour rendre le son moins agréable
                if wave > 0:
                    wave = min(wave * 1.5, 0.3)  # Sature le signal positif
                
                sample = int(wave * 32767)
                error_sound.append([sample, sample])
            
            error_array = np.array(error_sound, dtype=np.int16)
            self.sounds['error'] = pygame.sndarray.make_sound(error_array)
            print("Son d'erreur créé")
            
            # === SON DE BONNE RÉPONSE (note montante douce) ===
            correct_sound = []
            for i in range(int(frames * 0.5)):  # Plus court que les autres
                time = float(i) / sample_rate
                freq = 300 + (i / (frames * 0.5)) * 150  # Monte de 300Hz à 450Hz
                wave = math.sin(2 * math.pi * freq * time) * 0.2
                
                # Effet d'adoucissement progressif
                fade_out = 1 - (i / (frames * 0.5)) * 0.3
                sample = int(wave * fade_out * 32767)
                correct_sound.append([sample, sample])
            
            correct_array = np.array(correct_sound, dtype=np.int16)
            self.sounds['correct'] = pygame.sndarray.make_sound(correct_array)
            print("Son de bonne réponse créé")
            
            # === SON DE DÉFAITE (accord mineur dramatique) ===
            defeat_sound = []
            defeat_frames = int(frames * 0.8)  # Plus long pour l'effet dramatique
            for i in range(defeat_frames):
                time = float(i) / sample_rate
                
                # Accord de La mineur (dramatique)
                freq1 = 220  # La (fondamentale)
                freq2 = 262  # Do (tierce mineure)
                freq3 = 330  # Mi (quinte)
                
                # Combine les trois notes de l'accord
                wave1 = math.sin(2 * math.pi * freq1 * time) * 0.4
                wave2 = math.sin(2 * math.pi * freq2 * time) * 0.3
                wave3 = math.sin(2 * math.pi * freq3 * time) * 0.2
                
                # Effet de decay (diminution progressive du volume)
                decay = 1 - (i / defeat_frames) * 0.7
                sample = int((wave1 + wave2 + wave3) * decay * 32767)
                defeat_sound.append([sample, sample])
            
            defeat_array = np.array(defeat_sound, dtype=np.int16)
            self.sounds['defeat'] = pygame.sndarray.make_sound(defeat_array)
            print("Son de défaite créé")
            
            # === VÉRIFICATION DES SONS CRÉÉS ===
            print("Test des sons créés...")
            for sound_name, sound in self.sounds.items():
                if sound is not None:
                    print(f"✓ {sound_name}: OK")
                else:
                    print(f"✗ {sound_name}: ERREUR")
            
            print("Effets sonores créés avec succès !")
                
        except ImportError as e:
            print(f"Erreur d'import numpy: {e}")
            self.sounds = {}  # Pas de sons si numpy n'est pas disponible
        except Exception as e:
            print(f"Erreur lors de la création des effets sonores: {e}")
            import traceback
            traceback.print_exc()  # Affiche la trace complète de l'erreur
            self.sounds = {}
    
    def play_sound(self, sound_name):
        """
        Joue un effet sonore spécifique
        
        Args:
            sound_name: nom du son à jouer ('victory', 'error', 'correct', 'defeat')
        """
        # === VÉRIFICATIONS PRÉALABLES ===
        if not self.sound_enabled:
            print(f"Son désactivé - {sound_name} non joué")
            return
            
        if not hasattr(self, 'sounds'):
            print("Aucun système de sons disponible")
            return
            
        if sound_name not in self.sounds:
            print(f"Son {sound_name} non trouvé dans {list(self.sounds.keys())}")
            return
            
        if self.sounds[sound_name] is None:
            print(f"Son {sound_name} est None")
            return
            
        # === LECTURE DU SON ===
        try:
            print(f"Tentative de lecture du son: {sound_name}")
            self.sounds[sound_name].play()
            print(f"Son {sound_name} joué avec succès")
        except Exception as e:
            print(f"Erreur lors de la lecture du son {sound_name}: {e}")
            import traceback
            traceback.print_exc()
    
    def explode_falling_letters(self, letter_typed):
        """
        Fait exploser toutes les lettres tombantes identiques à celle tapée
        Crée un effet visuel spectaculaire avec des particules colorées
        
        Args:
            letter_typed: la lettre qui vient d'être tapée
            
        Returns:
            int: nombre de lettres qui ont explosé
        """
        # Détermine si la lettre est correcte pour choisir la couleur d'explosion
        is_correct_letter = letter_typed in self.word_to_guess
        explosion_color = GREEN if is_correct_letter else RED
        
        print(f"Recherche de lettres '{letter_typed}' qui tombent...")
        
        # === RECHERCHE ET EXPLOSION DES LETTRES IDENTIQUES ===
        explosion_count = 0
        for falling_letter in self.falling_letters:
            if falling_letter.letter == letter_typed:
                explosion_count += 1
                print(f"Explosion de la lettre {letter_typed} à la position ({falling_letter.x}, {falling_letter.y})")
                
                # === CRÉATION DE L'EXPLOSION DE PARTICULES ===
                for _ in range(15):  # 15 particules par explosion
                    # Vitesses aléatoires dans toutes les directions
                    velocity_x = random.uniform(-5, 5)
                    velocity_y = random.uniform(-8, -2)  # Principalement vers le haut
                    
                    # Ajoute la particule avec position légèrement aléatoire
                    self.particles.append(Particle(
                        falling_letter.x + random.randint(-10, 10),
                        falling_letter.y + random.randint(-10, 10),
                        explosion_color,
                        (velocity_x, velocity_y)
                    ))
                
                # === RÉINITIALISATION DE LA LETTRE EXPLOSÉE ===
                # Remet la lettre en haut avec de nouvelles propriétés
                falling_letter.y = random.randint(-200, -50)
                falling_letter.x = random.randint(0, WINDOW_WIDTH)
                falling_letter.letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                falling_letter.color = random.choice([LIGHT_BLUE, PURPLE, PINK, GREEN, YELLOW, WHITE])
                falling_letter.speed = random.uniform(1, 4)
                falling_letter.size = random.randint(32, 64)
                falling_letter.alpha = random.randint(200, 255)
                # Nettoie les effets visuels
                falling_letter.trail_positions.clear()
                falling_letter.particles.clear()
        
        # === RAPPORT DE L'EXPLOSION ===
        if explosion_count > 0:
            couleur_nom = 'VERTE' if is_correct_letter else 'ROUGE'
            print(f"💥 {explosion_count} lettre(s) {letter_typed} ont explosé avec couleur {couleur_nom}!")
        else:
            print(f"Aucune lettre {letter_typed} ne tombait à l'écran")
        
        return explosion_count
    
    def reset_game(self):
        """
        Remet le jeu à zéro pour commencer une nouvelle partie
        Sélectionne un nouveau mot et réinitialise tous les états
        """
        # === SÉLECTION DU NOUVEAU MOT ===
        word_and_category = self.get_word_to_guess()
        self.word_to_guess = word_and_category[0]  # Le mot à deviner
        self.category = word_and_category[1]       # Sa catégorie
        
        # === RÉINITIALISATION DES VARIABLES DE JEU ===
        self.guessed_letters = set()     # Lettres déjà proposées
        self.wrong_letters = set()       # Lettres incorrectes uniquement
        self.penalties = 0               # Nombre d'erreurs
        self.max_penalties = 10          # Maximum autorisé
        self.game_over = False           # État de fin de jeu
        self.won = False                 # Victoire ou défaite
        self.show_category_hint = False  # Affichage de l'indice de catégorie
        self.hints_used = 0              # Nombre d'indices utilisés
        
        print(f"Nouveau mot: {self.word_to_guess} (Catégorie: {self.category})")
    
    def give_hint(self):
        """
        Système d'indices qui révèle des lettres contre une pénalité
        Révèle 1 lettre si le mot fait moins de 6 caractères, 2 sinon
        Ajoute 5 pénalités en malus
        """
        if self.game_over:  # Pas d'indice si le jeu est terminé
            return
        
        # === DÉTERMINATION DU NOMBRE DE LETTRES À RÉVÉLER ===
        letters_to_reveal = 1 if len(self.word_to_guess) < 6 else 2
        
        # === RECHERCHE DES LETTRES NON DEVINÉES ===
        unrevealed_letters = []
        for letter in set(self.word_to_guess):  # set() évite les doublons
            if letter not in self.guessed_letters:
                unrevealed_letters.append(letter)
        
        # Vérification de sécurité
        if not unrevealed_letters:
            print("Toutes les lettres sont déjà révélées !")
            return
        
        # === RÉVÉLATION ALÉATOIRE DES LETTRES ===
        # Choisit aléatoirement parmi les lettres non révélées
        letters_revealed = random.sample(unrevealed_letters, 
                                       min(letters_to_reveal, len(unrevealed_letters)))
        
        # Ajoute les lettres révélées aux lettres devinées
        for letter in letters_revealed:
            self.guessed_letters.add(letter)
        
        # === APPLICATION DU MALUS ===
        self.penalties += 5  # Pénalité pour avoir utilisé un indice
        self.hints_used += 1  # Compteur d'indices
        
        # === AFFICHAGE DE L'INDICE ===
        if len(letters_revealed) == 1:
            print(f"INDICE: Lettre révélée: {letters_revealed[0]} (+5 pénalités)")
        else:
            print(f"INDICE: Lettres révélées: {', '.join(letters_revealed)} (+5 pénalités)")
        
        # === VÉRIFICATION DE VICTOIRE AVEC INDICE ===
        if all(letter in self.guessed_letters for letter in self.word_to_guess):
            self.won = True
            self.game_over = True
            print("VICTOIRE AVEC INDICE - Lancement du son de victoire")
            self.play_sound('victory')
            
            # Explosion de particules colorées pour célébrer
            for _ in range(50):
                colors = [YELLOW, LIGHT_BLUE, PURPLE, PINK, GREEN]
                self.add_particles(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 
                                 random.choice(colors))
        
        # === VÉRIFICATION DE DÉFAITE PAR MALUS ===
        elif self.penalties >= self.max_penalties:
            self.game_over = True
            print("DEFAITE PAR INDICE - Lancement du son de défaite")
            self.play_sound('defeat')
    
    def toggle_sound(self):
        """
        Active ou désactive le système audio complet
        """
        self.sound_enabled = not self.sound_enabled
        
        if self.sound_enabled:  # === ACTIVATION ===
            # Relance la musique de fond
            if hasattr(self, 'background_music'):
                self.background_music.play(loops=-1)
                self.background_music.set_volume(self.music_volume)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.unpause()
        else:  # === DÉSACTIVATION ===
            # Arrête la musique de fond
            if hasattr(self, 'background_music'):
                self.background_music.stop()
            else:
                pygame.mixer.music.pause()
    
    def adjust_volume(self, delta):
        """
        Ajuste le volume de la musique de fond
        
        Args:
            delta: changement de volume (-0.1 pour baisser, +0.1 pour monter)
        """
        # Maintient le volume entre 0.0 et 1.0
        self.music_volume = max(0.0, min(1.0, self.music_volume + delta))
        
        # Applique le nouveau volume si le son est activé
        if self.sound_enabled:
            if hasattr(self, 'background_music'):
                self.background_music.set_volume(self.music_volume)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
    
    def draw_options_panel(self, screen):
        """
        Dessine le panneau d'options avec roue dentée animée
        Permet de contrôler le volume et l'état du son
        
        Returns:
            tuple: (gear_x, gear_y, gear_radius) pour la détection de clic
        """
        # === DIMENSIONS ET POSITION DU PANNEAU ===
        panel_width = 250
        panel_height = 150
        panel_x = WINDOW_WIDTH - panel_width - 20  # En haut à droite
        panel_y = 20
        
        # === ROUE DENTÉE CLIQUABLE (ICÔNE D'OPTIONS) ===
        gear_radius = 20
        gear_x = panel_x + panel_width - 30
        gear_y = panel_y + 30
        
        # Animation de rotation continue
        rotation = self.animation_time * 0.02
        
        # === DESSIN DE LA ROUE DENTÉE ===
        # Couleur change selon l'état du panneau
        gear_color = YELLOW if self.show_options else LIGHT_BLUE
        
        # Cercle principal de la roue
        pygame.draw.circle(screen, gear_color, (gear_x, gear_y), gear_radius)
        pygame.draw.circle(screen, BLACK, (gear_x, gear_y), gear_radius, 2)
        
        # === DENTS DE LA ROUE (8 DENTS) ===
        for i in range(8):
            angle = rotation + i * (math.pi / 4)  # 45° entre chaque dent
            # Position externe de la dent
            outer_x = gear_x + math.cos(angle) * (gear_radius + 8)
            outer_y = gear_y + math.sin(angle) * (gear_radius + 8)
            # Position interne (sur le cercle)
            inner_x = gear_x + math.cos(angle) * gear_radius
            inner_y = gear_y + math.sin(angle) * gear_radius
            # Dessine la dent
            pygame.draw.line(screen, gear_color, (inner_x, inner_y), (outer_x, outer_y), 4)
        
        # === CERCLE CENTRAL ===
        pygame.draw.circle(screen, BLACK, (gear_x, gear_y), 8)   # Contour
        pygame.draw.circle(screen, gear_color, (gear_x, gear_y), 6)  # Remplissage
        
        # === PANNEAU D'OPTIONS (si activé) ===
        if self.show_options:
            # === CRÉATION DU PANNEAU AVEC TRANSPARENCE ===
            options_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            pygame.draw.rect(options_surface, (*DARK_BLUE, 200), (0, 0, panel_width, panel_height), border_radius=15)
            pygame.draw.rect(options_surface, WHITE, (0, 0, panel_width, panel_height), 2, border_radius=15)
            
            # === TITRE DU PANNEAU ===
            title_text = self.small_font.render("OPTIONS", True, WHITE)
            options_surface.blit(title_text, (10, 10))
            
            # === CONTRÔLE DU SON ON/OFF ===
            sound_label = self.small_font.render("Son:", True, WHITE)
            options_surface.blit(sound_label, (10, 40))
            
            # Affichage de l'état avec couleur appropriée
            sound_status = "ON" if self.sound_enabled else "OFF"
            sound_color = GREEN if self.sound_enabled else RED
            sound_text = self.small_font.render(sound_status, True, sound_color)
            options_surface.blit(sound_text, (60, 40))
            
            # === CONTRÔLE DU VOLUME ===
            volume_label = self.small_font.render("Volume:", True, WHITE)
            options_surface.blit(volume_label, (10, 70))
            
            # === BARRE DE VOLUME INTERACTIVE ===
            volume_bar_x = 10
            volume_bar_y = 100
            volume_bar_width = 200
            volume_bar_height = 20
            
            # Fond gris de la barre
            pygame.draw.rect(options_surface, DARK_GRAY, 
                           (volume_bar_x, volume_bar_y, volume_bar_width, volume_bar_height), 
                           border_radius=10)
            
            # === PROGRESSION DU VOLUME (si son activé) ===
            if self.sound_enabled:
                progress_width = int(self.music_volume * volume_bar_width)
                # Couleur selon le niveau de volume
                if self.music_volume > 0.5:
                    volume_color = GREEN      # Fort = vert
                elif self.music_volume > 0.2:
                    volume_color = YELLOW     # Moyen = jaune
                else:
                    volume_color = RED        # Faible = rouge
                    
                pygame.draw.rect(options_surface, volume_color,
                               (volume_bar_x, volume_bar_y, progress_width, volume_bar_height),
                               border_radius=10)
            
            # === CURSEUR DE VOLUME ===
            cursor_x = volume_bar_x + int(self.music_volume * volume_bar_width) - 5
            pygame.draw.circle(options_surface, WHITE, 
                             (cursor_x + 5, volume_bar_y + volume_bar_height // 2), 8)
            pygame.draw.circle(options_surface, LIGHT_BLUE, 
                             (cursor_x + 5, volume_bar_y + volume_bar_height // 2), 6)
            
            # === POURCENTAGE DU VOLUME ===
            volume_percent = f"{int(self.music_volume * 100)}%"
            percent_text = self.small_font.render(volume_percent, True, WHITE)
            options_surface.blit(percent_text, (volume_bar_x + volume_bar_width + 10, volume_bar_y - 5))
            
            # Colle le panneau sur l'écran principal
            screen.blit(options_surface, (panel_x, panel_y))
        
        return gear_x, gear_y, gear_radius  # Retourne les coordonnées pour la détection de clic
    
    def handle_options_click(self, mouse_pos, gear_x, gear_y, gear_radius):
        """
        Gère tous les clics sur le système d'options
        
        Args:
            mouse_pos: position du clic de souris (x, y)
            gear_x, gear_y, gear_radius: coordonnées de la roue dentée
            
        Returns:
            bool: True si un élément d'option a été cliqué
        """
        # === CLIC SUR LA ROUE DENTÉE ===
        # Calcule la distance entre le clic et le centre de la roue
        distance = math.sqrt((mouse_pos[0] - gear_x) ** 2 + (mouse_pos[1] - gear_y) ** 2)
        if distance <= gear_radius + 10:  # Marge de 10 pixels pour faciliter le clic
            self.show_options = not self.show_options  # Inverse l'affichage
            return True
        
        # === CLICS DANS LE PANNEAU D'OPTIONS (si ouvert) ===
        if self.show_options:
            panel_x = WINDOW_WIDTH - 250 - 20
            panel_y = 20
            volume_bar_x = panel_x + 10
            volume_bar_y = panel_y + 100
            volume_bar_width = 200
            volume_bar_height = 20
            
            # === CLIC SUR LA BARRE DE VOLUME ===
            if (volume_bar_x <= mouse_pos[0] <= volume_bar_x + volume_bar_width and
                volume_bar_y <= mouse_pos[1] <= volume_bar_y + volume_bar_height):
                
                # Calcule le nouveau volume basé sur la position X du clic
                relative_x = mouse_pos[0] - volume_bar_x
                new_volume = relative_x / volume_bar_width
                self.music_volume = max(0.0, min(1.0, new_volume))  # Limite entre 0 et 1
                
                # Applique immédiatement le nouveau volume
                if self.sound_enabled:
                    if hasattr(self, 'background_music'):
                        self.background_music.set_volume(self.music_volume)
                    else:
                        pygame.mixer.music.set_volume(self.music_volume)
                return True
            
            # === CLIC SUR LE BOUTON ON/OFF DU SON ===
            if (panel_x + 60 <= mouse_pos[0] <= panel_x + 120 and
                panel_y + 40 <= mouse_pos[1] <= panel_y + 60):
                self.toggle_sound()  # Active/désactive le son
                return True
        
        return False  # Aucun élément d'option cliqué
    
    def add_particles(self, x, y, color, count=10):
        """
        Ajoute des particules d'effet à une position donnée
        
        Args:
            x, y: position où créer les particules
            color: couleur des particules
            count: nombre de particules à créer (défaut: 10)
        """
        for _ in range(count):
            # Vitesse aléatoire pour chaque particule
            velocity = (random.uniform(-3, 3), random.uniform(-5, -1))
            self.particles.append(Particle(x, y, color, velocity))
    
    def guess_letter(self, letter):
        """
        Traite la proposition d'une lettre par le joueur
        Gère les explosions de lettres tombantes et les effets sonores
        
        Args:
            letter: lettre proposée (en majuscule)
            
        Returns:
            bool: True si la lettre était valide à proposer
        """
        # === VÉRIFICATIONS PRÉALABLES ===
        if letter in self.guessed_letters or self.game_over:
            return False  # Lettre déjà proposée ou jeu terminé
        
        # === EXPLOSION DES LETTRES TOMBANTES ===
        # Fait exploser toutes les lettres identiques qui tombent
        explosions = self.explode_falling_letters(letter)
        if explosions > 0:
            print(f"💥 {explosions} lettre(s) {letter} ont explosé !")
        
        # === TRAITEMENT DE LA LETTRE ===
        self.guessed_letters.add(letter)  # Ajoute à la liste des lettres proposées
        
        if letter not in self.word_to_guess:  # === LETTRE INCORRECTE ===
            self.wrong_letters.add(letter)  # Ajoute aux lettres fausses
            self.penalties += 1             # Incrémente les erreurs
            # Effets visuels et sonores pour l'erreur
            self.add_particles(WINDOW_WIDTH // 2, 300, RED)
            self.play_sound('error')
        else:  # === LETTRE CORRECTE ===
            # Effets visuels et sonores pour le succès
            self.add_particles(WINDOW_WIDTH // 2, 500, GREEN)
            self.play_sound('correct')
        
        # === VÉRIFICATION DE VICTOIRE ===
        # Vérifie si toutes les lettres du mot ont été devinées
        if all(letter in self.guessed_letters for letter in self.word_to_guess):
            self.won = True
            self.game_over = True
            print("VICTOIRE DETECTEE - Lancement du son de victoire")
            self.play_sound('victory')
            
            # Explosion de particules colorées pour célébrer
            for _ in range(50):
                colors = [YELLOW, LIGHT_BLUE, PURPLE, PINK, GREEN]
                self.add_particles(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 
                                 random.choice(colors))
        
        # === VÉRIFICATION DE DÉFAITE ===
        if self.penalties >= self.max_penalties:
            self.game_over = True
            print("DEFAITE DETECTEE - Lancement du son de défaite")
            self.play_sound('defeat')
        
        return True  # La lettre était valide
    
    def update(self):
        """
        Met à jour tous les éléments animés du jeu à chaque frame
        """
        self.animation_time += 1  # Incrémente le compteur global d'animation
        
        # === MISE À JOUR DES PARTICULES D'EFFETS ===
        # Garde seulement les particules encore vivantes
        self.particles = [p for p in self.particles if p.life > 0]
        # Met à jour chaque particule restante
        for particle in self.particles:
            particle.update()
        
        # === MISE À JOUR DES LETTRES TOMBANTES ===
        for letter in self.falling_letters:
            letter.update()
    
    def draw(self, screen):
        """
        Dessine tout l'interface du jeu sur l'écran
        Gère l'ordre de rendu pour les effets de profondeur
        
        Returns:
            tuple: coordonnées de la roue dentée pour la détection de clic
        """
        # === ARRIÈRE-PLAN DÉGRADÉ ===
        draw_gradient_background(screen)
        
        # === LETTRES TOMBANTES (ARRIÈRE-PLAN) ===
        # Dessine en premier pour qu'elles soient derrière tout le reste
        for letter in self.falling_letters:
            letter.draw(screen, self.letter_font)
        
        # === TITRE PRINCIPAL AVEC EFFET BRILLANT ===
        # Couleur qui change dans le temps (cycle de 3 couleurs)
        title_color = [LIGHT_BLUE, PURPLE, PINK][int(self.animation_time * 0.02) % 3]
        title = self.big_font.render("PENDU DELUXE", True, title_color)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        
        # === EFFET DE HALO BRILLANT ===
        glow = pygame.Surface(title.get_size(), pygame.SRCALPHA)
        glow.blit(title, (0, 0))
        # Dessine plusieurs copies décalées pour l'effet de halo
        for i in range(5):
            glow_pos = (title_rect.x - i, title_rect.y - i)
            screen.blit(glow, glow_pos)
        screen.blit(title, title_rect)  # Titre principal par-dessus
        
        # === INDICE DE CATÉGORIE (si activé) ===
        if self.show_category_hint:
            cat_text = self.small_font.render(f"Catégorie: {self.category}", True, YELLOW)
            screen.blit(cat_text, (WINDOW_WIDTH // 2 - cat_text.get_width() // 2, 100))
        
        # === BONHOMME PENDU ANIMÉ ===
        draw_animated_stickman(screen, self.penalties, self.animation_time)
        
        # === MOT À DEVINER AVEC ANIMATIONS ===
        draw_word_display(screen, self.word_to_guess, self.guessed_letters, 
                         self.medium_font, self.animation_time)
        
        # === PANNEAU D'INFORMATIONS ===
        # Crée un panneau semi-transparent pour les informations de jeu
        info_panel = pygame.Surface((300, 250), pygame.SRCALPHA)
        pygame.draw.rect(info_panel, (*DARK_BLUE, 150), (0, 0, 300, 250), border_radius=15)
        pygame.draw.rect(info_panel, WHITE, (0, 0, 300, 250), 2, border_radius=15)
        
        # === COMPTEUR D'ERREURS AVEC BARRE DE PROGRESSION ===
        penalty_text = self.small_font.render("Erreurs:", True, WHITE)
        info_panel.blit(penalty_text, (10, 10))
        
        # Barre de progression visuelle des erreurs
        bar_width = 200
        bar_height = 20
        bar_x, bar_y = 10, 40
        
        # Fond gris de la barre
        pygame.draw.rect(info_panel, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        
        if self.penalties > 0:  # Si il y a des erreurs
            # Calcule la largeur de progression
            progress_width = int((self.penalties / self.max_penalties) * bar_width)
            
            # Couleur selon le niveau de danger
            if self.penalties > 7:
                color = RED       # Critique (rouge)
            elif self.penalties > 4:
                color = YELLOW    # Attention (jaune)
            else:
                color = GREEN     # Ça va (vert)
                
            pygame.draw.rect(info_panel, color, (bar_x, bar_y, progress_width, bar_height), border_radius=10)
        
        # Texte avec le décompte précis
        penalty_count = self.small_font.render(f"{self.penalties}/{self.max_penalties}", True, WHITE)
        info_panel.blit(penalty_count, (bar_x + bar_width + 10, bar_y - 5))
        
        # === LETTRES INCORRECTES ===
        if self.wrong_letters:
            wrong_text = self.small_font.render("Lettres fausses:", True, RED)
            info_panel.blit(wrong_text, (10, 80))
            
            # Affiche toutes les lettres fausses triées par ordre alphabétique
            wrong_display = " ".join(sorted(self.wrong_letters))
            wrong_letters_surf = self.small_font.render(wrong_display, True, WHITE)
            info_panel.blit(wrong_letters_surf, (10, 110))
        
        # === COMPTEUR D'INDICES UTILISÉS ===
        hint_text = self.small_font.render(f"Indices: {self.hints_used}", True, YELLOW)
        info_panel.blit(hint_text, (10, 140))
        
        # === AIDE POUR LES INDICES ===
        if not self.game_over:
            hint_info = self.small_font.render("F4 = Indice (+5 pénalités)", True, GRAY)
            info_panel.blit(hint_info, (10, 160))
        
        # Colle le panneau d'infos sur l'écran
        screen.blit(info_panel, (650, 150))
        
        # === PANNEAU D'OPTIONS ===
        gear_x, gear_y, gear_radius = self.draw_options_panel(screen)
        
        # === PARTICULES D'EFFETS ===
        # Dessine toutes les particules actives par-dessus tout le reste
        for particle in self.particles:
            particle.draw(screen)
        
        # === MESSAGES DE FIN DE JEU ===
        if self.game_over:
            # === OVERLAY SEMI-TRANSPARENT ===
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 100), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            screen.blit(overlay, (0, 0))
            
            if self.won:  # === ÉCRAN DE VICTOIRE ===
                # Animation de pulsation pour "VICTOIRE!"
                scale = 1 + math.sin(self.animation_time * 0.1) * 0.1  # ±10% de variation
                
                # Redimensionne dynamiquement le texte
                original_size = self.big_font.size("VICTOIRE!")
                scaled_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                
                win_text = pygame.transform.scale(
                    self.big_font.render("VICTOIRE!", True, YELLOW),
                    scaled_size
                )
                win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                screen.blit(win_text, win_rect)
                
                # Message de félicitations
                congrats = self.medium_font.render("Félicitations!", True, GREEN)
                screen.blit(congrats, (WINDOW_WIDTH // 2 - congrats.get_width() // 2, win_rect.bottom + 20))
                
            else:  # === ÉCRAN DE DÉFAITE ===
                defeat_text = self.big_font.render("DÉFAITE!", True, RED)
                defeat_rect = defeat_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                screen.blit(defeat_text, defeat_rect)
                
                # Révèle le mot correct
                word_text = self.medium_font.render(f"Le mot était: {self.word_to_guess}", True, WHITE)
                screen.blit(word_text, (WINDOW_WIDTH // 2 - word_text.get_width() // 2, defeat_rect.bottom + 20))
            
            # === INSTRUCTIONS POUR REJOUER ===
            controls_text = self.small_font.render("F5 = Rejouer | F4 = Indice | F6 = Options | ESC = Quitter", True, LIGHT_BLUE)
            screen.blit(controls_text, (WINDOW_WIDTH // 2 - controls_text.get_width() // 2, WINDOW_HEIGHT - 100))
        
        return gear_x, gear_y, gear_radius  # Coordonnées pour la détection de clic

def main():
    """
    Fonction principale qui lance et gère la boucle de jeu complète
    Initialise pygame, crée le jeu et gère tous les événements
    """
    # === INITIALISATION DE PYGAME ===
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pendu Deluxe - Version Graphique Avancée")
    clock = pygame.time.Clock()  # Contrôle de la vitesse du jeu
    
    # === CRÉATION DU JEU ===
    game = HangmanDeluxe()  # Instance de la classe principale
    running = True          # Variable pour contrôler la boucle
    gear_coords = (0, 0, 0) # Coordonnées de la roue dentée pour les clics
    
    # === AFFICHAGE DES INSTRUCTIONS ===
    print("=== PENDU DELUXE ===")
    print("Commandes:")
    print("• Lettres A-Z : Deviner")
    print("• F5 : Nouvelle partie")
    print("• F4 : Indice (révèle 1-2 lettres, +5 pénalités)")
    print("• F6 : Options (volume, son)")
    print("• ESC : Quitter")
    
    # === BOUCLE PRINCIPALE DU JEU ===
    while running:
        # === GESTION DES ÉVÉNEMENTS ===
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:  # Fermeture de fenêtre
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Clic de souris
                if event.button == 1:  # Clic gauche uniquement
                    # Tente de gérer le clic sur les options
                    game.handle_options_click(event.pos, *gear_coords)
            
            elif event.type == pygame.KEYDOWN:  # Pression de touche
                
                if event.key == pygame.K_ESCAPE:  # Échap = quitter
                    running = False
                    
                elif event.key == pygame.K_F5:  # F5 = nouvelle partie
                    game.reset_game()
                    
                elif event.key == pygame.K_F4:  # F4 = indice
                    game.give_hint()
                    
                elif event.key == pygame.K_F6:  # F6 = toggle options
                    game.show_options = not game.show_options
                    
                # === GESTION DES LETTRES ===
                elif not game.game_over and pygame.K_a <= event.key <= pygame.K_z:
                    # Seulement si le jeu n'est pas terminé et que c'est une lettre
                    letter = chr(event.key).upper()  # Convertit en majuscule
                    game.guess_letter(letter)        # Traite la proposition
        
        # === MISE À JOUR ET AFFICHAGE ===
        game.update()                           # Met à jour toutes les animations
        gear_coords = game.draw(screen)         # Dessine tout et récupère les coordonnées de la roue
        pygame.display.flip()                  # Actualise l'affichage
        clock.tick(FPS)                        # Maintient 60 FPS
    
    # === NETTOYAGE À LA SORTIE ===
    pygame.quit()  # Ferme pygame proprement
    sys.exit()     # Termine le processus Python

# === POINT D'ENTRÉE DU PROGRAMME ===
if __name__ == "__main__":
    """
    Condition qui vérifie si le script est exécuté directement
    (et non importé comme module)
    """
    main()  # Lance la fonction principale