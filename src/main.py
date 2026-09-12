import ui


def main():
    while True:
        option = ui.auth_menu()

        match option:
            case 1:
                current_user = ui.login_user()

                if current_user:
                    while True:
                        agenda_personal = current_user.agenda
                        option = ui.menu()

                        if option == 0:
                            print("\nCerrando Sesión...\n")
                            break

                        match option:
                            case 1:
                                ui.add_contact(agenda_personal)

                            case 2:
                                ui.show_contacts(agenda_personal)

                            case 3:
                                print("\nBUSCAR CONTACTO")

                                ui.find_contact(agenda_personal)

                            case 4:
                                ui.update_contact(agenda_personal)

                            case 5:
                                ui.delete_contact(agenda_personal)

                            case 6:
                                ui.call_contact(agenda_personal)

                            case _:
                                print('\nCerrando Sesión...\n')
                                break
            case 2:
                ui.register_ui()
            case _:
                print("\nSaliendo del sistema. ¡Hasta pronto!...\n")
                break


if __name__ == '__main__':
    main()
