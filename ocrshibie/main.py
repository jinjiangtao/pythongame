from app import OCRApp

def main():
    app = OCRApp()
    try:
        app.run()
    finally:
        app.close()

if __name__ == "__main__":
    main()
