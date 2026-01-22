import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.1
MOVE_SPEED = 1
JUMP_SPEED = 6.5
COYOTE_TIME = 0.08
JUMP_BUFFER = 0
MAX_JUMPS = 1
CAMERA_LERP = 0.15
MAX_SPEED = 6
ACCSELERATION = 0.1
MOVE = 0
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Аркадный Бегун", fullscreen=True)
        arcade.set_background_color(arcade.color.BLUE)

        # Спрайт игрока
        self.player = arcade.Sprite(
            "sprites/character/Idle.png", scale=2)
        self.idle = arcade.load_texture(
            "sprites/character/Idle.png")
        self.idlel = arcade.load_texture(
            "sprites/character/Idlel.png")
        self.player.center_x = 200
        self.player.center_y = 200
        self.player_spritelist = arcade.SpriteList()
        self.player_spritelist.append(self.player)
        self.player_list = arcade.SpriteList()
        self.tile_map = arcade.load_tilemap("map/green.tmx",
                                            scaling=2)
        self.ground = self.tile_map.sprite_lists["ground"]
        self.invis = self.tile_map.sprite_lists["invisible"]
        self.plat = self.tile_map.sprite_lists["platforms"]
        self.death = self.tile_map.sprite_lists["die"]
        self.hide = self.tile_map.sprite_lists["hide"]
        self.touch = self.tile_map.sprite_lists["touch"]
        self.walk_right = []
        self.walk_left = []
        self.last_move = 1
        self.run_right = []
        self.run_left = []
        self.jump = []
        for i in range(4):
            texture = arcade.load_texture(f"sprites/character/walk{i + 1}.png")
            self.walk_right.append(texture)
            texture = arcade.load_texture(f"sprites/character/walkl{i + 1}.png")
            self.walk_left.append(texture)
            texture = arcade.load_texture(f"sprites/character/jump{i + 1}.png")
            self.jump.append(texture)
            texture = arcade.load_texture(f"sprites/character/run{i + 1}.png")
            self.run_right.append(texture)
            texture = arcade.load_texture(f"sprites/character/runl{i + 1}.png")
            self.run_left.append(texture)
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.current_texture = 0
        self.is_walkingr = self.is_walkingl = False
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, (self.ground, self.invis, self.plat))
        self.spawn_point = (200, 200)
        self.left = self.right = self.up = self.down = self.jump_pressed = self.stopl = self.stopr = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=(self.ground, self.plat)
        )
        self.batch = Batch()
        self.text_info = arcade.Text("WASD/стрелки — ходьба/лестницы • SPACE — прыжок",
                                     16, 16, arcade.color.GRAY, 14, batch=self.batch)

    def setup(self):
        self.player.center_x, self.player.center_y = self.spawn_point
        self.player_list.append(self.player)
        self.jump_buffer_timer = 0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

    def on_draw(self):
        self.clear()
        self.player_spritelist.draw()
        self.ground.draw()
        self.world_camera.use()
        self.plat.draw()
        self.hide.draw()


    def on_update(self, dt: float):
        global MOVE
        if self.left and not self.right:
            if MOVE > -MAX_SPEED:
                MOVE += -MOVE_SPEED * ACCSELERATION

        elif self.right and not self.left:
            if MOVE < MAX_SPEED:
                MOVE += MOVE_SPEED * ACCSELERATION

        if self.stopr and not self.stopl:
            MOVE += -MOVE_SPEED * 0.3
            if MOVE < 0:
                MOVE = 0
                self.stopr = False
        elif self.stopl and not self.stopr:
            MOVE += MOVE_SPEED * 0.3
            if MOVE > 0:
                MOVE = 0
                self.stopl = False

        if arcade.check_for_collision_with_list(self.player, self.hide):
            print("YES")

        if arcade.check_for_collision_with_list(self.player, self.death):
            self.player.center_x, self.player.center_y = self.spawn_point
            self.player.change_x = self.player.change_y = 0
            self.time_since_ground = 999
            self.jumps_left = MAX_JUMPS

        if self.is_walkingr or self.is_walkingl:
            self.texture_change_time += 0.039
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if MOVE < 6:
                    if self.current_texture >= len(self.walk_right):
                        self.current_texture = 0
                elif MOVE >= 6:
                    if self.current_texture >= len(self.run_right):
                        self.current_texture = 0
                if self.is_walkingr:
                    if MOVE < 6:
                        self.player.texture = self.walk_right[self.current_texture]
                    else:
                        self.player.texture = self.run_right[self.current_texture]
                elif self.is_walkingl:
                    if MOVE > -6:
                        self.player.texture = self.walk_left[self.current_texture]
                    else:
                        self.player.texture = self.run_left[self.current_texture]
        else:
            if self.last_move == 1:
                self.player.texture = self.idle
            elif self.last_move == -1:
                self.player.texture = self.idlel

        self.player.change_x = MOVE
        self.player.change_y -= GRAVITY
        grounded = self.engine.can_jump(y_distance=6)
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.texture_change_time += 0.039
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
            if self.current_texture >= len(self.jump):
                self.current_texture = 0
            self.player.texture = self.jump[self.current_texture]
            self.time_since_ground += dt
        position = (
            self.player.center_x,
            self.player.center_y
        )
        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)
        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                self.engine.jump(JUMP_SPEED)
                self.jump_buffer_timer = 0
        self.engine.update()
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position, position, CAMERA_LERP)
        self.physics_engine.update()
        target = (self.player.center_x, self.player.center_y)
        cx, cy = self.world_camera.position
        smooth = (cx + (target[0] - cx) * CAMERA_LERP,
                  cy + (target[1] - cy) * CAMERA_LERP)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        world_w = 10000
        world_h = 900
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))

        self.world_camera.position = (cam_x, cam_y)



    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
            self.stopl = False
            self.is_walkingl = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
            self.stopr = False
            self.is_walkingr = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

    def on_key_release(self, key, modifiers):
        global MOVE
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
            self.stopl = True
            self.is_walkingl = False
            self.last_move = -1
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
            self.stopr = True
            self.is_walkingr = False
            self.last_move = 1
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.45


def main():
    game = MyGame()
    arcade.run()



if __name__ == "__main__":
    main()