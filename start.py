
import embed.config as config
from embed.gpio import Server

def main():
    """Main boilerplate."""
    server = Server.from_file(
        fname=config.GPIOConfig.FILENAME,
        addr=config.NetworkConfig.HOST,
        num_workers=5
    )
    server.listen(port=config.NetworkConfig.PORT)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

    
    
