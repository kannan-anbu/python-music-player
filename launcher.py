from gui import gui_main
from mediastore.musicstore import MusicStore

ms = MusicStore()
ms.init()
ms.build()
# ms.reset()
ms.close()

gui_main.startApp()

