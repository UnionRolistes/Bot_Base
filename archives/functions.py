"""
Ci-dessous se trouvent les trois commandes qui étaient demandées dans un ticket. Voici une description de ces dernières :
    • name : change le nickname du bot sur le serveur où est tapée la commande. Le nom initial (qui apparaît sur chaque serveur) ne change pas.
Pourtant, il est possible de changer ce dernier. Cependant, Discord y impose une limite (deux changements par heure).
→ Faudrait-il garder la première option ou coder la deuxième ; faire les deux ?

    • description : change le message d'état de présence du bot.
On ne peut malheureusement pas changer la section "À propos de moi" par une commande.
De plus, tout comme un utilisateur lambda ne pourrait pas le faire, un même bot ne peut pas posséder plusieurs statuts différents selon les serveurs.

    • pfp : change la photo de profil du bot en vérifiant l'URL et en retournant les requêtes appropriés.


D'ailleurs, on ne peut vérifier l'ID du serveur qu'à l'intérieur des fonctions, car c'est en recevant une commande, que le bot peut connaître le serveur d'où est tapée cette dernière. C'est pourquoi il subsiste une répétition des lignes
suivantes : "server_id = ctx.guild.id" & "guild = bot.get_guild(server_id)".
Ces deux commandes récupèrent l'ID du serveur d'où est tapée la commande.
Ce sont elles qui permettent pour un même bot d'avoir un nom ou une photo de profil différente selon les serveurs.


Ces programmes ont donc bien été retiré du code fonctionnel. En revanche, leur code est laissé ci-dessous, si le besoin
de s'en inspirer se présente.
"""
# import aiohttp


# Fonction pour lire la description depuis le fichier
# def read_description_from_file():
#     try:
#         with open('description.txt', 'r') as file:
#             # ↓ De quel fichier ?, ↓ Quelle permission ?
#             return file.read().strip()
#     except FileNotFoundError:
#         return ""
#
#
# # Fonction pour écrire la description dans le fichier
# def write_description_to_file(texte):
#     with open('description.txt', 'w') as file:
#         # ↓ De quel fichier ?, ↓ Quelle permission ?
#         file.write(texte)
#
# async def on_ready(self):
#     print('--- We have successfully logged in as {0.user}'.format(self))
#     # Lire la description depuis le fichier et mettre à jour la présence du bot
#     bot.description = read_description_from_file()
#     await update_bot_presence()
#
#
# # Commande pour changer le pseudo du bot
# @bot.command()
# async def name(ctx, *, new_name: str):
#     server_id = ctx.guild.id
#
#     try:
#         guild = bot.get_guild(server_id)
#
#         if guild:
#             # Changer le pseudo du bot sur le serveur spécifié
#             await guild.me.edit(nick=new_name)
#             await ctx.send(f"Le pseudo du bot a bien été changé en {new_name}.")
#         else:
#             await ctx.send("Impossible de trouver le serveur spécifié.")
#
#     except discord.HTTPException as e:
#         await ctx.send("Une erreur s'est produite lors du changement de pseudo du bot. Veuillez regarder la console.")
#         print(e)
#
#
# # Fonction qui met à jour automatiquement (et en permanence) le statut personnalisé du bot.
# async def update_bot_presence():
#     activity = discord.Game(name=bot.description)  # Ces deux lignes doivent être appelées en permanence par
#     await bot.change_presence(activity=activity)  # la fonction on_ready. C'est pourquoi elles ne sont pas écrites dans
#     # la commande 'description'.
#
#
# # Commande pour changer le statut personnalisé du bot.
# @bot.command()
# async def description(ctx, *, texte: str):
#     bot.description = texte
#     write_description_to_file(texte)
#     await update_bot_presence()
#     await ctx.send(f"La description du bot a été mise à jour.")
#
#
# # Commande pour changer la photo de profil du bot.
# @bot.command()
# async def pfp(ctx, *, url: commands.clean_content):
#     try:
#         server_id = ctx.guild.id
#         guild = bot.get_guild(server_id)
#
#         if guild:
#             # Récupération de l'image.
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url) as resp:  # Malgré l'erreur, le code fonctionne toujours.
#                     if resp.status != 200:
#                         return await ctx.send(f"Impossible de télécharger l'image. Statut HTTP : {resp.status}")
#
#                     # La photo de profil prend la forme de l'image.
#                     data = await resp.read()
#                     await bot.user.edit(avatar=data)
#                     await ctx.send("Photo de profil mise à jour. Redémarrez le bot pour voir le résultat.")
#         else:
#             # Attraper toutes les erreurs possibles.
#             await ctx.send("Impossible de trouver le serveur discord spécifié. Veuillez contactez les développeurs du projet.")
#     except aiohttp.InvalidURL:
#         await ctx.send("L'URL fournie est invalide. Veuillez vérifier qu'elle ne contient pas de guillemet, "
#                        "ni d'apostrophe et réessayer.")
#     except Exception as e:
#         await ctx.send(f"Une erreur s'est produite : {str(e)} Vérifiez votre configuration du bot ou contactez "
#                        f"les développeurs du projet.")
