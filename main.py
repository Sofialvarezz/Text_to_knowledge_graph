from Pipeline import TextToGraphPipeline 
from UI import KnowledgeGraphApp
import tkinter as tk


while True:
    
    print("Selecciona el modo de ejecución:")
    print("1. Interfaz gráfica")
    print("2. Consola")
    print("3. Salir")
    opcion = input("Introduce el número de tu opción: ")

    if opcion == '1':
        root = tk.Tk()
        app = KnowledgeGraphApp(root)
        root.mainloop()
        break

    elif opcion == '2':
        text = ""
        file_name= ""
        while True:
            print("\n")
            print("¿Desea ingresar un texto, usar el texto predeterminado o seleccionar el texto de un archivo?")
            print("1. Ingresar texto (500 caracteres)")
            print("2. Usar texto predeterminado")
            print("3. Salir del programa")
            opcion_texto = input("Introduce el número de tu opción: ")


            if opcion_texto == '1':
                while True:  
                    text = input("\nIntroduce el texto (menos de 500 caracteres): ")
                    if len(text) <= 500:
                        break  
                    else:
                        print("\nEl texto excede los 500 caracteres. Por favor, inténtalo nuevamente.")


            elif opcion_texto == '2':
                text = "La Revolución Industrial marcó el inicio de la mecanización en Inglaterra, Francia y Alemania. La invención de la máquina de vapor por James Watt transformó sectores como la minería y el transporte. Ciudades como Manchester y Birmingham se convirtieron en centros industriales. Esto impulsó la economía mundial en el siglo XIX."
                break


            elif opcion_texto == '3':
                print("Saliendo del programa...")
                break

            else:
                print("Opción no válida. Por favor, selecciona una opción válida.")

        if text:
            print(f"Texto introducido: {text}")
            pipeline = TextToGraphPipeline()
            pipeline.create_graph(text, file_name)
        break

    elif opcion == '3':
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")


