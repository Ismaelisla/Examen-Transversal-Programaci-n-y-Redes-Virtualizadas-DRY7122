def verificar_rango_vlan(numero_vlan):
    if 1 <= numero_vlan <= 1000:
        print(f"La VLAN {numero_vlan} pertenece al rango normal.")
    elif 1002 <= numero_vlan <= 4094:
        print(f"La VLAN {numero_vlan} pertenece al rango extendido.")
    else:
        print(f"La VLAN {numero_vlan} no es válida.")
        
def main():
    vlan = int(input("Ingrese el número de VLAN: "))
    verificar_rango_vlan(vlan)
    
if __name__ == "__main__":
    main()
