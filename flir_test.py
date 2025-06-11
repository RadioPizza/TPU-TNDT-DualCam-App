import PySpin
system = PySpin.System.GetInstance()
cam_list = system.GetCameras()
print('Number of cameras:', cam_list.GetSize())
cam_list.Clear()
system.ReleaseInstance()