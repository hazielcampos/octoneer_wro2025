from src.components.Servo import set_angle, CENTER_POSITION, LEFT_POSITION, RIGHT_POSITION, disable as disable_servo

try:
    set_angle(CENTER_POSITION)
    while True:
        angle = int(input("Enter servo angle: "))
        set_angle(angle)
        
except KeyboardInterrupt:
    print("User interrupted")