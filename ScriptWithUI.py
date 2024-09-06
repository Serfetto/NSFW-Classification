# Import library
import threading
from PIL import ImageGrab
from ultralytics import YOLO
import obspython as obs
import torch

#Global variables
list_ids_of_source = ["monitor_capture", "game_capture", "dshow_input", "window_capture"]

path_to_model = ""
model = None

scene_name = ""
scene = None
scene_item = None

width = 0
height = 0

filter_name = "filter nsfw"
id_filter_name = None
is_filter = False

stop_thread = False
nsfw_thread = None


#For obs
def script_defaults(settings):
    print("Script defaults")

    obs.obs_data_set_default_string(settings, "path_to_model", "")
    obs.obs_data_set_default_string(settings, "scene_name", "")


def script_update(settings):
    print("Script update")
    global path_to_model, scene_name

    path_to_model = obs.obs_data_get_string(settings, "path_to_model")
    scene_name = obs.obs_data_get_string(settings, "scene_name")


def script_properties():
    print("Script properties")
    props = obs.obs_properties_create()

    obs.obs_properties_add_path(props, "path_to_model", "Path to model:", obs.OBS_PATH_FILE, None, script_path())

    list_1 = obs.obs_properties_add_list(props, "scene_name", "Select scene:", obs.OBS_COMBO_TYPE_LIST,
                                         obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_clear(list_1)

    scenes = obs.obs_frontend_get_scenes()
    for new_scene in scenes:
        scene_name = obs.obs_source_get_name(new_scene)
        obs.obs_property_list_add_string(list_1, scene_name, scene_name)
    obs.source_list_release(scenes)

    obs.obs_properties_add_button(props, "start_filter", "Start filtering", start_analyze)
    obs.obs_properties_add_button(props, "stop_filter", "Stop filtering", stop_analyze)

    return props


def script_load(settings):
    print("Script load")
    obs.obs_data_set_string(settings, "scene_name", "")


def script_unload():
    print("Script unload")


def create_filter():
    global id_filter_name, scene, scene_item

    scene = obs.obs_scene_from_source(obs.obs_get_source_by_name(scene_name))

    color_settings = obs.obs_data_create()
    obs.obs_data_set_int(color_settings, "color", 0xFF000000)
    obs.obs_data_set_int(color_settings, "width", width)
    obs.obs_data_set_int(color_settings, "height", height)
    color_source = obs.obs_source_create_private("color_source", filter_name, color_settings)
    obs.obs_scene_add(scene, color_source)

    for item in obs.obs_scene_enum_items(scene):
        source = obs.obs_sceneitem_get_source(item)
        if (obs.obs_source_get_name(source) == filter_name) and (obs.obs_source_get_id(source) == "color_source"):
            scene_item = item
            break


def delete_filter():
    obs.obs_sceneitem_remove(obs.obs_scene_find_source(scene, filter_name))


def connecting_model():
    global model

    model = YOLO(path_to_model, task='classify')
    torch.cuda.set_device(0)

    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    model.to(device)


def screen_monitor():
    return ImageGrab.grab()


def get_video_resolution():
    global width, height
    width, height = ImageGrab.grab().size


def classify_nsfw():
    global stop_thread, scene_item

    connecting_model()

    while not stop_thread:
        image = screen_monitor()

        output = model.predict(image, verbose=False)[0]

        probs = torch.sort(output.probs.data)

        out = {output.names[idx]: f"{prob:.3f}" for idx, prob in zip(probs.indices.tolist(), probs.values.tolist())}

        print(out)

        if float(out['nsfw']) > 0.65:
            obs.obs_sceneitem_set_visible(scene_item, True)
        else:
            obs.obs_sceneitem_set_visible(scene_item, False)


def start_analyze(props, prop):
    global stop_thread, nsfw_thread

    get_video_resolution()

    create_filter()

    print("Launching NSFW content recognition")
    stop_thread = False
    nsfw_thread = threading.Thread(target=classify_nsfw).start()


def stop_analyze(props, prop):
    global stop_thread, nsfw_thread
    print("\nStopping NSFW content recognition")

    stop_thread = True
    if nsfw_thread is not None:
        nsfw_thread.join()
        nsfw_thread = None

    delete_filter()

