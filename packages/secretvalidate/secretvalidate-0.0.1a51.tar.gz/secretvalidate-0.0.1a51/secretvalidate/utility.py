import subprocess

from secretvalidate.env_loader import get_packagename

# Custom type function to convert input to lowercase
def lowercase_choice(value):
    return value.lower()

def format_services(services):
    """Format service choices as a bullet-point list."""
    return "\n".join([f"  - {service}" for service in services])

def update_tool():
    """Update the tool to the latest version."""
    try:
        subprocess.run(["pip", "install", "--upgrade",
                       f"{get_packagename()}"], check=True)
        print("Tool updated to the latest version.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update the tool: {e}")
