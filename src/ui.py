from datetime import datetime

from auth_manager import AuthManager
from config import CATEGORIES
from exceptions.blocked_user_error import BlockedUserError
from exceptions.contact_not_found_error import ContactNotFoundError
from exceptions.duplicate_phone_error import DuplicatePhoneError
from exceptions.duplicate_user_error import DuplicateUserError
from exceptions.user_not_found_error import UserNotFoundError
from models.agenda import Agenda
from models.contact import Contact
from models.user import User


def auth_menu():
    MENU_AUTH = '''
    --- SISTEMA DE SEGURIDAD ---
    
    [1] Iniciar sesión
    [2] Registrarse
    [3] Salir
    '''

    print(MENU_AUTH)
    return get_valid_option('Seleccione una opción: ', (1, 2, 3))


def register_ui() -> None:
    try:
        name = get_name_user("Ingrese su nombre: ")
        lastname = get_lastname("Ingrese su apellido: ")
        email = get_email("Ingrese su email: ")
        username = get_username("Ingrese el nombre de usuario: ")
        password = get_password("Ingrese su contraseña: ")

        user = User(name, lastname, username, email, password)

        AuthManager.register_user(user)
        print(f"\nEl usuario {username} ha sido registrado correctamente.")

    except DuplicateUserError as e:
        print(f"\nError: {e.message}. {e.details}")
        print("Por favor, intente registrarse nuevamente.\n")


def login_user() -> User | None:
    print("\n--- INICIAR SESIÓN ---")

    attempts = 0
    max_attempts = 3
    username = input("Ingrese su nombre de usuario: ").strip()

    while attempts < max_attempts:
        password = input("Ingrese su contraseña: ").strip()

        try:
            current_user = AuthManager.login_user(username, password)
            print(f"\n¡Bienvenido {current_user.name} {current_user.lastname}!")

            return current_user

        except UserNotFoundError as e:
            print(f"\nError: {e.message}. {e.details}\n")
            return None
        except BlockedUserError as e:
            print(f"\nError: {e.message}. {e.details}\n")
            return None
        except ValueError as e:
            attempts += 1

            if attempts >= max_attempts:
                AuthManager.lock_user(username)

                print(f"\nError: Máximo de intentos agotados.")
                return None
            else:
                print(f"\nError: {e}")
                print("Por favor, ingrese sus datos correctos.\n")

    return None


def menu() -> int:
    OPTIONS_MENU = f'''
    --- Opciones - Agenda de Contactos ---

    [1] Agregar un nuevo contacto
    [2] Ver lista de contactos
    [3] Buscar contacto
    [4] Actualizar contacto
    [5] Eliminar contacto
    [6] Llamar contacto
    [0] Cerrar sesión
    '''

    print(OPTIONS_MENU)
    return get_valid_option('Seleccione una opción: ', (1, 2, 3, 4, 5, 6, 0))


def get_name_contact(prompt: str = "Ingrese el nombre: "):
    return get_name(prompt)


def get_phone_contact(prompt: str = "Ingrese el teléfono: "):
    while True:
        phone = input(prompt)

        if not phone.strip() or len(phone) != 9:
            print("\nEl teléfono debe tener exactamente 9 números. Por favor, ingrese un teléfono válido.\n")
        else:
            return phone.strip()


def get_email(prompt: str = "Ingrese el email: "):
    while True:
        email = input(prompt)

        if not email.strip() or len(email) < 12:
            print("\nEl email debe tener entre 12 caracteres mínimo. Por favor, ingrese un email válido.\n")
        else:
            return email.strip()


def get_category_contact():
    while True:
        print("Categorías:")
        for key, category in enumerate(CATEGORIES):
            print(f"\t[{key + 1}] {category}")

        category = input(f"Seleccione la categoría ({'/'.join(CATEGORIES)}): ")

        try:
            category = int(category) - 1

            if category >= len(CATEGORIES) or category < 0:
                print(
                    "\nEl número ingresado no identifica a ninguna categoría en la lista de categorías",
                    "Por favor, ingrese un número válido de categoría.\n")
            else:
                return CATEGORIES[category]
        except ValueError:
            print(
                "\nEl número de categoría debe ser un número. Por favor, ingrese un número válido de categoría.\n")


def create_contact() -> Contact:
    print("\nAGREGAR DATOS DEL NUEVO CONTACTO\n")

    name = get_name_contact()
    phone = get_phone_contact()
    email = get_email()
    category = get_category_contact()

    return Contact(name, phone, email, category)


def add_contact(agenda: Agenda) -> None:
    while True:
        contact = create_contact()

        try:
            agenda.add_contact(contact)
            print(f"\nEl contacto '{contact.name}' ha sido agregado.")

            if not should_continue("¿Desea agregar otro contacto? (s/n): "):
                break
        except DuplicatePhoneError as e:
            print(f"\nError: {e.message}. {e.details}")
            print("Por favor, intente registrar de nuevo.\n")


def search_menu() -> int:
    SEARCH_MENU = '''
        --- Opciones de búsqueda ---

        [1] Nombre
        [2] Email
        [3] Teléfono
        '''
    print(SEARCH_MENU)

    return get_valid_option('Seleccione una opción: ', (1, 2, 3))


def find_contact(agenda: Agenda) -> None:
    choice = search_menu()

    match choice:
        case 1:
            name = input("Ingrese el nombre a buscar: ").strip()

            contacts_found = agenda.find_by_name(name)

            if not contacts_found:
                print(f"\nNo hay contactos con ese nombre: {name}\n")

            show_contacts(agenda, contacts_found)
        case 2:
            email = input("Ingrese el email a buscar: ").strip()

            contacts_found = agenda.find_by_email(email)

            if not contacts_found:
                print(f"\nNo hay contactos con ese email: {email}\n")

            show_contacts(agenda, contacts_found)
        case _:
            phone = input("Ingrese el teléfono a buscar: ").strip()

            contacts_found = agenda.find_by_phone(phone)

            if not contacts_found:
                print(f"\nNo hay contactos con ese teléfono: {phone}\n")

            show_contacts(agenda, contacts_found)


def show_contacts(agenda: Agenda, contacts: list[Contact] | None = None) -> None:
    contacts_to_show = agenda.get_contacts() if contacts is None else contacts

    if not contacts_to_show:
        print("\nNo hay contactos registrados. Por favor, registra uno primero.\n")
        return

    print("\nLISTA DE CONTACTOS:")

    for i, contact in enumerate(contacts_to_show, start=1):
        print(f"\t{i}. {contact.name} - {contact.phone} - {contact.email} - {contact.category}")

        created = format_relative_time(contact.created_at)
        updated = format_relative_time(contact.updated_at)
        print(f"\t   [Creado: {created} | Editado: {updated}]")
    print()


def get_position_contact(prompt: str, contact_list_size: int) -> int:
    while True:
        try:
            position = int(input(prompt))

            if 1 <= position <= contact_list_size:
                return position - 1

            print(f"\nPosición incorrecta. Por favor, Ingrese una posición entre 1 y {contact_list_size}.\n")
        except ValueError:
            print('\nEntrada inválida. Por favor, ingrese un número.\n')


def call_contact(agenda: Agenda) -> None:
    show_contacts(agenda)

    if not agenda.get_contacts():
        print("\nNo hay ningún contacto registrado. Por favor, registra uno primero.\n")
        return

    while True:
        position = get_position_contact(
            'Seleccione una posición del contacto a llamar: ',
            len(agenda.get_contacts())
        )

        contact = agenda.call_contact(position)
        print(f"\nLlamando a {contact.name}: 📞 {contact.phone} ~~~~\n")

        if not should_continue("¿Desea seguir llamando? (s/n): "):
            break


def delete_contact(agenda: Agenda) -> None:
    show_contacts(agenda)

    while True:
        if not agenda.get_contacts():
            print("\nNo hay ningún contacto registrado. Por favor, registra uno primero.\n")
            break

        position = get_position_contact(
            "Seleccione una posición del contacto a eliminar: ",
            len(agenda.get_contacts())
        )

        try:
            agenda.delete_contact(position)
            print("\nContacto eliminado correctamente.\n")
            break
        except ContactNotFoundError as e:
            print(f"\nError: {e.message}. {e.details}")


def update_contact(agenda: Agenda) -> None:
    show_contacts(agenda)

    if not agenda.get_contacts():
        print('\nNo hay ningún contacto registrado. Por favor, registra uno primero.\n')
        return

    position = get_position_contact(
        'Seleccione una posición del contacto a actualizar: ',
        len(agenda.get_contacts())
    )

    while True:
        if not agenda.get_contact_by_index(position):
            print("\n\nPosición incorrecta del contacto. Por favor, digite una posición de un contacto existente.\n")
            continue
        else:

            try:
                contact = agenda.get_contact_by_index(position)

                if not contact:
                    print('\nError: No se encontró el contacto. Por favor, verifique que exista.\n')
                    return

                choice = get_update_field_option()

                match choice:
                    case 1:
                        name = get_name_contact('Ingrese el nuevo nombre: ')
                        contact.name = name

                    case 2:
                        email = get_email('Ingrese el nuevo email: ')
                        contact.email = email

                    case 3:
                        while True:
                            phone = get_phone_contact('Ingrese el nuevo teléfono: ')

                            agenda.validate_new_phone_number(contact.phone, phone)
                            contact.phone = phone

                print('\n\nContacto actualizado correctamente.\n')
                break
            except (DuplicatePhoneError, ContactNotFoundError) as e:
                print(f"\nError: {e.message}.\n{e.details}\n")
                break


def get_valid_option(prompt: str, valid_options: tuple) -> int:
    while True:
        try:
            option = int(input(prompt))

            if option in valid_options:
                return option

            print(f'Opción incorrecta. Opciones válidas: {valid_options}')
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")


def get_update_field_option():
    UPDATE_MENU = '''
                --- Campo a actualizar ---

                [1] Nombre
                [2] Email
                [3] Teléfono
                '''
    print(UPDATE_MENU)

    return get_valid_option('Seleccione una opción: ', (1, 2, 3))


def should_continue(prompt: str) -> bool:
    choice = input(f'\n{prompt}')

    if choice.strip().lower() != "s":
        return False

    return True


def format_relative_time(date_obj: datetime) -> str:
    diff = datetime.now() - date_obj
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "hace un momento"
    elif seconds < 3600:
        minutes = seconds // 60

        return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600

        return f"hace {hours} hora{'s' if hours > 1 else ''}"
    else:
        days = seconds // 86400

        return f"hace {days} día{'s' if days > 1 else ''}"


def get_name(prompt: str = "Ingrese el nombre: "):
    while True:
        name = input(prompt)

        if not name.strip() or len(name) < 2:
            print(
                "\nEl nombre no puede estar vacío o tener menos de 2 letras. Por favor, ingrese un nombre válido.\n")
        else:
            return name.strip()


# Funciones para trabajar con el usuario

def get_name_user(prompt: str = "Ingrese el nombre"):
    return get_name(prompt)


def get_lastname(prompt: str = "Ingrese el apellido: "):
    while True:
        lastname = input(prompt)

        if not lastname.strip() or len(lastname) < 2:
            print(
                "\nEl apellido no puede estar vacío o tener menos de 2 letras. Por favor, ingrese un apellido válido.\n")
        else:
            return lastname.strip()


def get_username(prompt: str = "Ingrese el nombre de usuario: "):
    while True:
        username = input(prompt)

        if not username.strip() or len(username) < 3:
            print(
                "\nEl nombre de usuario no puede estar vacío o tener menos de 3 letras. Por favor, ingrese un nombre de usuario válido.\n")
        else:
            return username.strip()


def get_password(prompt: str = "Ingrese la contraseña: "):
    while True:
        password = input(prompt)

        if not password.strip() or len(password) < 6:
            print("\nLa contraseña debe tener al menos 6 caracteres. Por favor, ingrese una contraseña válida.\n")
        else:
            return password.strip()
