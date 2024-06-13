from pypylon import pylon


tlf = pylon.TlFactory.GetInstance()
tl = tlf.CreateTl("BaslerUsb")
dev = tl.CreateFirstDevice()
cap = pylon.InstantCamera()
cap.Attach(dev)
cap.Open()
cap.StartGrabbing()
# cap.DeviceTemperatureSelector.Value = 'Sensor'
print(cap.DeviceTemperatureSelector.Value)
cap.StopGrabbing()
cap.DestroyDevice()
# while True:
#     print(cap.DeviceTemperature.Value)
