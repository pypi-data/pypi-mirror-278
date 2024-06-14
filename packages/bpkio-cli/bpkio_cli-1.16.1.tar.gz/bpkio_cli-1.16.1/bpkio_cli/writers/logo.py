import click


def show_logo():
    click.secho(
        """
                             xxxxxxxxx                             
                           xxxx    xxxx                            
                           xxx      xxxx                           
                           xxx      xxxx                           
                           xxxx    xxxx                            
                             xxxxxxxxx                             
                                   xxx                             
                                   xxx                             
                 xxxxxxxxxxxxx     xxx                             
              xxxxxxxx   xxxxxxxx xxx                              
             xxxxx           xxxxxxxx             xxx              
              x                xxxxxx           xxxxxx             
                               xxxxxxxxxxxxxxxxxxxx                
                   xxxxxxxxxxxxxx      xxxxxxx                     
              xxxxxxxxxxxxxxxxxx                                   
             xxxxx          xxxxxxx                xx              
             xxx            xxxxxxxxx            xxxxx             
                            xxx   xxxxxxx    xxxxxxx               
                             xxx      xxxxxxxxxxx                  
                             xxxx                                  
                              xxxx                                 
                               xxx          """,
        fg="yellow",
    )

    click.secho(
        """                               
     ___                  _                _     _        ___ _    ___ 
    | _ )_ _ ___  __ _ __| |_ __  ___ __ _| |__ (_)___   / __| |  |_ _|
    | _ \ '_/ _ \/ _` / _` | '_ \/ -_) _` | / /_| / _ \ | (__| |__ | | 
    |___/_| \___/\__,_\__,_| .__/\___\__,_|_\_(_)_\___/  \___|____|___|
                            |_|                                         
    """,
        fg="blue",
        bold=True,
    )
