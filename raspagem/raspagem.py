import sys
import time
import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_inteiro(texto):
	try:
		i = texto.rindex(' ')
		sem_unidade = texto[:i]

		# Às vezes, esse valor pode iniciar pelo ano...
		i = sem_unidade.find(' ')
		if i >= 0:
			sem_unidade = sem_unidade[(i + 1):]

		sem_virgula = sem_unidade.replace(',', '')

		return int(sem_virgula)
	except:
		return 0

driver = webdriver.Chrome()
driver.get(config.url_inicial)


links = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ipc-title > a.ipc-title-link-wrapper'))
)

filmes = []

for i in range(0, 20):
	filmes.append({
		"url": links[i].get_attribute("href"),
		"titulo": "",
		"duracao": "",
		"ano": 0,
		"classificacao_etaria": "",
		"nota": 0,
		"posicao": i + 1,
		"generos": [],
		"atores": [],
	})
	
for contador_filme in range(20):
	filme = filmes[contador_filme]
	driver.get(filme["url"])

	time.sleep(1)

	body = driver.find_element(By.TAG_NAME, 'body')

	for i in range(15):
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(2)

	titulo = WebDriverWait(driver, 1).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hero__primary-text'))
	)

	filme["titulo"] = titulo.text.strip()

	meta = WebDriverWait(driver, 1).until(
		EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-af040695-0.iOwuHP > ul > li'))
	)

	if len(meta) > 0:
		filme["ano"] = int(meta[0].text.strip())
		if len(meta) > 1:
			filme["classificacao_etaria"] = meta[1].text.strip()
			if len(meta) > 2:
				filme["duracao"] = meta[2].text.strip()

	try:
		nota = WebDriverWait(driver, 5).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.sc-4dc495c1-1.lbQcRY'))
		)

		filme["nota"] = float(nota[0].text.strip().replace(",", "."))
	except:
		filme["nota"] = 0

	for i in range(3):
		try:
			generos = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-testid="storyline-genres"] div a'))
			)
			break
		except:
			body.send_keys(Keys.PAGE_UP)
			time.sleep(0.5)
			body.send_keys(Keys.PAGE_UP)
			time.sleep(0.5)
			body.send_keys(Keys.PAGE_UP)
			time.sleep(0.5)
			body.send_keys(Keys.PAGE_UP)
			time.sleep(0.5)
			body.send_keys(Keys.PAGE_UP)
			time.sleep(0.5)

	filme["generos"] = []
	filme["atores"] = []

	for genero in generos:
		filme["generos"].append(genero.text.strip())

	atores = WebDriverWait(driver, 1).until(
		EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ipc-shoveler.title-cast__grid a[data-testid="title-cast-item__actor"]'))
	)

	for ator in atores:
		filme["atores"].append(ator.text.strip())
		

driver.close()