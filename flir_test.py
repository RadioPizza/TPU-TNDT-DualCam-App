import PySpin
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_flir_camera():
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()
    
    if num_cameras == 0:
        logger.error("No FLIR cameras found.")
        return
    
    camera = cam_list.GetByIndex(0)
    camera.Init()
    
    # Set camera settings
    nodemap = camera.GetNodeMap()
    
    # Disable binning and decimation
    for node_name in ['BinningHorizontal', 'BinningVertical', 
                     'DecimationHorizontal', 'DecimationVertical']:
        node = PySpin.CIntegerPtr(nodemap.GetNode(node_name))
        if PySpin.IsAvailable(node) and PySpin.IsWritable(node):
            node.SetValue(1)
            logger.info(f"Set {node_name} to 1")

    # Set maximum resolution
    node_width = PySpin.CIntegerPtr(nodemap.GetNode("Width"))
    node_height = PySpin.CIntegerPtr(nodemap.GetNode("Height"))
    node_width_max = PySpin.CIntegerPtr(nodemap.GetNode("WidthMax"))
    node_height_max = PySpin.CIntegerPtr(nodemap.GetNode("HeightMax"))

    if all(PySpin.IsAvailable(node) for node in [node_width, node_height, node_width_max, node_height_max]):
        width_max = node_width_max.GetValue()
        height_max = node_height_max.GetValue()
        
        node_width.SetValue(width_max)
        node_height.SetValue(height_max)
        logger.info(f"Set resolution to maximum: {width_max}x{height_max}")

    # Verify actual resolution
    width = node_width.GetValue()
    height = node_height.GetValue()
    logger.info(f"Final camera resolution: {width}x{height}")
    
    camera.BeginAcquisition()
    
    try:
        for i in range(10):
            image_result = camera.GetNextImage(1000)
            if image_result.IsIncomplete():
                logger.warning(f"Image incomplete with status: {image_result.GetImageStatus()}")
            else:
                image_data = image_result.GetNDArray()
                logger.info(f"Image shape: {image_data.shape}")
                logger.info(f"Pixel format: {image_result.GetPixelFormat()}")
                
                # Convert image based on pixel format
                pixel_format = image_result.GetPixelFormat()
                if pixel_format == PySpin.PixelFormat_Mono8:
                    rgb_image = cv2.applyColorMap(image_data, cv2.COLORMAP_JET)
                elif pixel_format == PySpin.PixelFormat_BayerBG8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_BG2BGR)
                elif pixel_format == PySpin.PixelFormat_BayerGB8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GB2BGR)
                elif pixel_format == PySpin.PixelFormat_BayerGR8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GR2BGR)
                elif pixel_format == PySpin.PixelFormat_BayerRG8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_BAYER_RG2BGR)
                elif pixel_format == PySpin.PixelFormat_BGR8:
                    rgb_image = image_data
                elif pixel_format == PySpin.PixelFormat_RGB8:
                    rgb_image = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
                else:
                    rgb_image = image_data
                
                cv2.imshow('FLIR Camera Test', rgb_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            image_result.Release()
    finally:
        camera.EndAcquisition()
        camera.DeInit()
        del camera
        cam_list.Clear()
        system.ReleaseInstance()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_flir_camera()