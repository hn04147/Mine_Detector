
mine_list=[]
int n=0

while n<11:
    int mine_x=random.randrange(0,11)
    int mine_y=random.randrange(0,11)
    screen.blit(mine,(mine_x*50,mine_y*50+100))
    mine_list.append(mine_x)
    mine_list.append(mine_y)
    n++
    
