
import generate_stats
import show_stats

def main():
    
    print("Generating `stats.json`")
    generate_stats.generate()
    print("Generated `stats.json`")

    print("Reading `stats.json`")
    show_stats.show()


if __name__ == "__main__":
    main()