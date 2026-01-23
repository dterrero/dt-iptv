import os
import subprocess

SOURCE_DIR = "/opt/iptv/sources/"
MAP_FILE_PATH = "/etc/nginx/conf.d/channel_map.map"

def generate_combined_map():
    channels_data = []
    
    # root = current folder, dirs = subfolders, files = files in current folder
    for root, dirs, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith(".txt"):
                # Construct full path to read the file
                file_path = os.path.join(root, filename)
                channel_id = filename.replace(".txt", "")
                
                try:
                    with open(file_path, "r") as f:
                        lines = f.read().splitlines()
                        if lines:
                            # The first line is your scraped .m3u8 URL
                            m3u8_url = lines[0]
                            # Use a SINGLE tilde (~) for NGINX regex
                            channels_data.append(f"    ~^/streams/{channel_id}/ \"{m3u8_url}\";")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    # Write the complete map file
    with open(MAP_FILE_PATH, "w") as f:
        f.write("map $request_uri $backend_url {\n")
        f.write("    default \"http://127.0.0.1/error\";\n\n")
        f.write("\n".join(channels_data))
        f.write("\n}\n")

    # Correct 'gninx' to 'nginx' and check configuration
    check = subprocess.run(["sudo", "nginx", "-t"], capture_output=True, text=True)
    if check.returncode == 0:
        subprocess.run(["sudo", "nginx", "-s", "reload"])
        print("Success: Combined map updated and NGINX reloaded.")
    else:
        print("Error: NGINX syntax check failed!")
        print(check.stderr)

if __name__ == "__main__":
    generate_combined_map()
