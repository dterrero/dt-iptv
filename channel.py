import os
import subprocess

SOURCE_DIR = "/opt/iptv/sources/"
MAP_FILE_PATH = "/etc/nginx/conf.d/channel_map.map"

def generate_map():
    channels_map = []
    
    # os.walk(dir) returns: (current_path, sub_folders, files_in_path)
    for root, dirs, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.endswith(".txt"):
                # Path to the file (e.g., /opt/iptv/sources/livetvde/msnbc.txt)
                file_path = os.path.join(root, filename)
                
                # Channel name is just the filename (e.g., msnbc)
                channel_name = filename.replace(".txt", "")
                
                try:
                    with open(file_path, "r") as f:
                        lines = f.read().splitlines()
                        if lines:
                            current_m3u8 = lines[0]
                            # Single tilde (~) for regex, escape the quotes
                            channels_map.append(f"~^/streams/{channel_name}/ \"{current_m3u8}\";")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    # Write to the file
    with open(MAP_FILE_PATH, "w") as f:
        f.write("map $request_uri $backend_url {\n")
        f.write("    default \"http://127.0.0.1/error\";\n")
        f.write("\n".join(channels_map))
        f.write("\n}\n")

    # Final Nginx check and reload
    # Make sure 'gninx' is corrected to 'nginx' here!
    result = subprocess.run(["sudo", "nginx", "-t"], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(["sudo", "nginx", "-s", "reload"])
        print("Success: Map updated and Nginx reloaded.")
    else:
        print("Error: Nginx config is invalid!")
        print(result.stderr)

if __name__ == "__main__":
    generate_map()
