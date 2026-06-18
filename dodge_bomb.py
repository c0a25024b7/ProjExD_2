import os
import random
import sys
import time
import pygame as pg

DELTA = {
    pg.K_UP: (0, -5),  # 上矢印キー
    pg.K_DOWN: (0, +5),  # 下矢印キー
    pg.K_LEFT: (-5, 0),  # 左矢印キー
    pg.K_RIGHT: (+5, 0),  # 右矢印キー
}

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    go_img = pg.Surface(screen.get_size()) 
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    txt_rct = txt.get_rect(center = (WIDTH//2,HEIGHT//2))
    go_img.blit(txt,txt_rct)
    kokaton = pg.image.load("fig/8.png")
    kokaton_rct1 = kokaton.get_rect(center = (WIDTH//2 - 200,HEIGHT//2))
    kokaton_rct2 = kokaton.get_rect(center = (WIDTH//2 + 200,HEIGHT//2))
    go_img.blit(kokaton,kokaton_rct1)
    go_img.blit(kokaton,kokaton_rct2)
    screen.blit(go_img,(0,0))
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 横初期座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦初期座標
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate:  
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
