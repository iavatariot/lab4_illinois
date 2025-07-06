#!/usr/bin/env python3
import time
import random
from pidog import Pidog
from preset_actions import bark

t = time.time()
my_dog = Pidog()
my_dog.do_action('stand', speed=80)
my_dog.wait_all_done()
time.sleep(.5)

DANGER_DISTANCE = 15
SCAN_ANGLES = [-60, -30, 0, 30, 60]  # Angoli per la scansione (sinistra a destra)

# Variabili per tracciare l'ultima azione e posizione testa
last_action = 'stand'
last_head_pitch = 0

# Azioni che richiedono di essere in piedi
STANDUP_ACTIONS = ['trot', 'forward', 'backward', 'turn_left', 'turn_right']

stand = my_dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])

def scan_for_distances():
    """Scansiona diverse direzioni per ottenere tutte le distanze"""
    distances = {}
    
    print("🔍 Scansionando ambiente...")
    # Scansiona diverse direzioni con più tempo per stabilizzarsi
    for angle in SCAN_ANGLES:
        # Muovi la testa verso l'angolo
        my_dog.head_move([[angle, 0, 0]], speed=80)
        my_dog.wait_all_done()
        time.sleep(0.4)  # Tempo maggiore per stabilizzarsi
        
        # Prendi multiple letture per maggiore precisione
        readings = []
        for _ in range(3):
            distance = my_dog.read_distance()
            if distance > 0:
                readings.append(distance)
            time.sleep(0.1)
        
        # Usa la lettura massima per evitare falsi positivi
        if readings:
            final_distance = max(readings)
            distances[angle] = round(final_distance, 2)
            print(f"  {angle:3d}°: {distances[angle]:5.1f} cm")
        else:
            distances[angle] = 0
            print(f"  {angle:3d}°: Nessuna lettura")
    
    # Riporta la testa al centro
    my_dog.head_move([[0, 0, 0]], speed=80)
    my_dog.wait_all_done()
    time.sleep(0.2)
    
    return distances

def find_best_direction_for_escape(distances):
    """Trova la direzione migliore per sfuggire a un ostacolo, preferendo lo spazio più ampio"""
    print("📊 Analizzando le distanze per fuga:")
    for angle, dist in distances.items():
        status = "✅ SICURO" if dist > DANGER_DISTANCE or dist == 0 else "⚠️ PERICOLOSO"
        print(f"    {angle:3d}°: {dist:5.1f} cm - {status}")
    
    # Filtra solo le direzioni sicure
    safe_directions = {angle: dist for angle, dist in distances.items() 
                      if dist > DANGER_DISTANCE or dist == 0}
    
    if not safe_directions:
        # Se non ci sono direzioni sicure, scegli quella con distanza maggiore
        best_angle = max(distances, key=distances.get)
        print(f"⚠️ Nessuna direzione completamente sicura, scelgo la migliore: {best_angle}°")
        return best_angle
    
    # Per la fuga, priorità assoluta allo spazio più ampio
    def calculate_escape_score(angle, dist):
        distance_score = 999 if dist == 0 else dist
        
        # Piccolo bonus per direzioni in avanti, ma priorità alla distanza
        if -30 <= angle <= 30:
            direction_bonus = 20  # Bonus moderato per avanti
        else:
            direction_bonus = 0   # Nessun bonus per laterale/indietro
        
        final_score = distance_score + direction_bonus
        print(f"    {angle:3d}°: distanza={dist} + bonus={direction_bonus} = score={final_score}")
        return final_score
    
    best_angle = max(safe_directions, key=lambda k: calculate_escape_score(k, safe_directions[k]))
    best_distance = safe_directions[best_angle]
    
    print(f"✅ Direzione migliore per fuga: {best_angle}° (distanza: {best_distance} cm)")
    return best_angle

def prepare_for_movement():
    """Prepara il Pidog per il movimento assicurandosi che sia in piedi"""
    global last_action, last_head_pitch
    
    # Se l'ultima azione non era un'azione di movimento, metti in piedi
    if last_action not in STANDUP_ACTIONS:
        print("Mettendo in piedi il Pidog...")
        my_dog.do_action('stand', speed=50)
        my_dog.wait_all_done()
        last_head_pitch = 0
        last_action = 'stand'
    
    # Assicurati che la testa sia in posizione neutra per il movimento
    my_dog.head_move_raw([[0, 0, last_head_pitch]], immediately=False, speed=60)

def turn_towards_direction(target_angle):
    """Gira il Pidog verso la direzione specificata - CORREZIONE: 
    target_angle positivo = gira a DESTRA, negativo = gira a SINISTRA"""
    global last_action, last_head_pitch
    
    # Prepara per il movimento
    prepare_for_movement()
    
    print(f"🎯 Girando verso {target_angle}° (spazio più ampio)")
    
    # CORREZIONE LOGICA: se target_angle è negativo (sinistra), gira a DESTRA per raggiungerlo
    # se target_angle è positivo (destra), gira a SINISTRA per raggiungerlo
    
    # Calcola l'angolo di rotazione necessario (opposto al target)
    rotation_angle = -target_angle
    
    # Logica di rotazione
    if rotation_angle <= -45:  # Dobbiamo girare molto a sinistra
        print("↰ Rotazione sinistra molto forte (4 step)")
        my_dog.do_action('turn_left', step_count=4, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_left'
    elif rotation_angle <= -25:  # Dobbiamo girare forte a sinistra
        print("↰ Rotazione sinistra forte (3 step)")
        my_dog.do_action('turn_left', step_count=3, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_left'
    elif rotation_angle < -10:  # Dobbiamo girare leggermente a sinistra
        print("↲ Rotazione sinistra leggera (2 step)")
        my_dog.do_action('turn_left', step_count=2, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_left'
    elif rotation_angle >= 45:  # Dobbiamo girare molto a destra
        print("↱ Rotazione destra molto forte (4 step)")
        my_dog.do_action('turn_right', step_count=4, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_right'
    elif rotation_angle >= 25:  # Dobbiamo girare forte a destra
        print("↱ Rotazione destra forte (3 step)")
        my_dog.do_action('turn_right', step_count=3, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_right'
    elif rotation_angle > 10:  # Dobbiamo girare leggermente a destra
        print("↳ Rotazione destra leggera (2 step)")
        my_dog.do_action('turn_right', step_count=2, speed=98, pitch_comp=last_head_pitch)
        last_action = 'turn_right'
    else:  # Direzione già abbastanza corretta
        print("↑ Direzione già corretta, piccola correzione")
        if rotation_angle > 0:
            my_dog.do_action('turn_right', step_count=1, speed=98, pitch_comp=last_head_pitch)
            last_action = 'turn_right'
        elif rotation_angle < 0:
            my_dog.do_action('turn_left', step_count=1, speed=98, pitch_comp=last_head_pitch)
            last_action = 'turn_left'
    
    my_dog.wait_all_done()
    time.sleep(0.2)

def do_backward_movement():
    """Esegue il movimento all'indietro con la preparazione corretta"""
    global last_action, last_head_pitch
    
    # Prepara per il movimento
    prepare_for_movement()
    
    print("↩️ Indietreggiando...")
    my_dog.do_action('backward', step_count=2, speed=98, pitch_comp=last_head_pitch)
    my_dog.wait_all_done()
    last_action = 'backward'

def do_forward_movement():
    """Esegue il movimento in avanti con la preparazione corretta"""
    global last_action, last_head_pitch
    
    # Prepara per il movimento se necessario
    if last_action not in STANDUP_ACTIONS:
        prepare_for_movement()
    
    my_dog.do_action('forward', step_count=2, speed=98, pitch_comp=last_head_pitch)
    my_dog.do_action('shake_head', step_count=1, speed=90)
    my_dog.do_action('wag_tail', step_count=5, speed=100)
    last_action = 'forward'

def patrol():
    distance = round(my_dog.read_distance(), 2)
    print(f"distance: {distance} cm", end="", flush=True)

    # danger - OSTACOLO RILEVATO
    if distance > 0 and distance < DANGER_DISTANCE:
        print("\033[0;31m DANGER !\033[m")
        my_dog.body_stop()
        head_yaw = my_dog.head_current_angles[0]
        
        # Effetti visivi e sonori
        my_dog.rgb_strip.set_mode('bark', 'red', bps=2)
        my_dog.tail_move([[0]], speed=80)
        my_dog.legs_move([stand], speed=70)
        my_dog.wait_all_done()
        time.sleep(0.5)
        
        # Abbaia (importante!)
        bark(my_dog, [head_yaw, 0, 0])
        
        # Indietreggia prima di scansionare (importante!)
        do_backward_movement()
        
        # Scansiona l'ambiente per trovare una via libera
        print("🔍 Scansionando l'ambiente per trovare una via libera...")
        distances = scan_for_distances()
        
        # Trova la direzione migliore per la fuga
        best_direction = find_best_direction_for_escape(distances)
        
        # Gira verso la direzione migliore
        turn_towards_direction(best_direction)
        
        # Verifica finale: dopo la rotazione, controlla se la direzione è davvero libera
        print("🔄 Verificando la nuova direzione...")
        time.sleep(0.5)
        final_distance = round(my_dog.read_distance(), 2)
        print(f"📏 Distanza finale dopo rotazione: {final_distance} cm")
        
        # Cambia colore LED per indicare che ha trovato una via
        if final_distance > DANGER_DISTANCE or final_distance == 0:
            my_dog.rgb_strip.set_mode('breath', 'green', bps=1)
            print("✅ Direzione libera confermata")
        else:
            my_dog.rgb_strip.set_mode('breath', 'yellow', bps=1)
            print("⚠️ Direzione ancora ostruita, continuerò con cautela")
        
        time.sleep(1)
        
    # safe - PERCORSO LIBERO
    else:
        print("")
        # Movimento normale senza scansione
        my_dog.rgb_strip.set_mode('breath', 'white', bps=0.5)
        do_forward_movement()


if __name__ == "__main__":
    try:
        print("🚀 Pidog Patrol - Scansione Solo in Pericolo!")
        print(f"📏 Distanza di pericolo: {DANGER_DISTANCE} cm")
        print("🧭 Strategia: Movimento normale dritto, scansione solo quando rileva ostacoli")
        while True:
            patrol()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n🛑 Patrol interrotto dall'utente")
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        print("🔌 Spegnendo Pidog...")
        my_dog.close()
        print("👋 Arrivederci!")
