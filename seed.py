from bs4 import BeautifulSoup
from models import Disc, Company
from app import db
import requests

counter = 0


db.drop_all()
db.create_all()


companies = {"innova": ["https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Innova&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0",
                        "https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=1&stmp=0&topx=100&sort=seller&sn=&stampname=&manufacturer%5B0%5D=Innova&type_name%5B0%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=0.0%7C7.0%7C0.0%7C7.0%7C0&disc_skill%5Bomin%5D=0.0&disc_skill%5Bomax%5D=7.0&disc_skill%5Bmin%5D=0.0&disc_skill%5Bmax%5D=7.0&disc_skill%5Bset%5D=0&disc_speed%5Bopt%5D=1.0%7C15.0%7C1.0%7C15.0%7C0&disc_speed%5Bomin%5D=1.0&disc_speed%5Bomax%5D=15.0&disc_speed%5Bmin%5D=1.0&disc_speed%5Bmax%5D=15.0&disc_speed%5Bset%5D=0&disc_glide%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_glide%5Bomin%5D=1.0&disc_glide%5Bomax%5D=7.0&disc_glide%5Bmin%5D=1.0&disc_glide%5Bmax%5D=7.0&disc_glide%5Bset%5D=0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_hss%5Bomin%5D=-5.0&disc_hss%5Bomax%5D=1.0&disc_hss%5Bmin%5D=-5.0&disc_hss%5Bmax%5D=1.0&disc_hss%5Bset%5D=0&disc_lss%5Bopt%5D=0.0%7C5.0%7C0.0%7C5.0%7C0&disc_lss%5Bomin%5D=0.0&disc_lss%5Bomax%5D=5.0&disc_lss%5Bmin%5D=0.0&disc_lss%5Bmax%5D=5.0&disc_lss%5Bset%5D=0&page=2",
                        "https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=1&stmp=0&topx=100&sort=seller&sn=&stampname=&manufacturer%5B0%5D=Innova&type_name%5B0%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=0.0%7C7.0%7C0.0%7C7.0%7C0&disc_skill%5Bomin%5D=0.0&disc_skill%5Bomax%5D=7.0&disc_skill%5Bmin%5D=0.0&disc_skill%5Bmax%5D=7.0&disc_skill%5Bset%5D=0&disc_speed%5Bopt%5D=1.0%7C15.0%7C1.0%7C15.0%7C0&disc_speed%5Bomin%5D=1.0&disc_speed%5Bomax%5D=15.0&disc_speed%5Bmin%5D=1.0&disc_speed%5Bmax%5D=15.0&disc_speed%5Bset%5D=0&disc_glide%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_glide%5Bomin%5D=1.0&disc_glide%5Bomax%5D=7.0&disc_glide%5Bmin%5D=1.0&disc_glide%5Bmax%5D=7.0&disc_glide%5Bset%5D=0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_hss%5Bomin%5D=-5.0&disc_hss%5Bomax%5D=1.0&disc_hss%5Bmin%5D=-5.0&disc_hss%5Bmax%5D=1.0&disc_hss%5Bset%5D=0&disc_lss%5Bopt%5D=0.0%7C5.0%7C0.0%7C5.0%7C0&disc_lss%5Bomin%5D=0.0&disc_lss%5Bomax%5D=5.0&disc_lss%5Bmin%5D=0.0&disc_lss%5Bmax%5D=5.0&disc_lss%5Bset%5D=0&page=3"],
                "discraft": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Discraft&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "lattitude 64": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Latitude+64&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "abc discs": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=ABC+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "axiom discs": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Axiom+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "dga": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=DGA&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "discmania" : ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Discmania&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "dynamic discs": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Dynamic+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "gateway": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Gateway&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "hyzer bomb": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Hyzer+Bomb&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "kastaplast": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Kastaplast&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "legacy discs": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Legacy+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "millenium": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Millennium&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "mvp": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=MVP+Disc+Sports&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "prodigy": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Prodigy+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "streamline": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Streamline+Discs&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0'],
                "westside": ['https://www.discgolfcenter.com/main_displayProductList.php?s=0&pl=0&oos=0&stmp=0&topx=100&sort=seller&sn=&stampname=&oos=1&manufacturer%5B%5D=Westside&type_name%5B%5D=Discs&weight%5Bmin%5D=&weight%5Bmax%5D=&disc_skill%5Bopt%5D=1.0%7C7.0%7C1.0%7C7.0%7C0&disc_speed%5Bopt%5D=1.0%7C14.5%7C1.0%7C14.5%7C0&disc_glide%5Bopt%5D=1.0%7C6.0%7C1.0%7C6.0%7C0&disc_hss%5Bopt%5D=-5.0%7C1.0%7C-5.0%7C1.0%7C0&disc_lss%5Bopt%5D=0.0%7C4.0%7C0.0%7C4.0%7C0']
                }


headers = {'User-Agent': 'Mozilla/5.0'}


for c, url in companies.items():
    new_c = Company(name=c)
    db.session.add(new_c)
    db.session.commit()


for c, urls in companies.items():

    for url in urls:
    
        response = requests.get(url, headers=headers).text

        soup = BeautifulSoup(response, 'lxml')
        discs = soup.find('ul', class_='large-block-grid-5 medium-block-grid-3 small-block-grid-2')

        for disc in discs.find_all('li'):
            try:
                disc_type = ''
                img = disc.find('img')['data-src']
                name_plastic = disc.find('div', class_='product-preview-title row').get_text(strip=True).split(" - ")
                name = name_plastic[0].lower()
                plastic = name_plastic[1].lower()
                difficulty = disc.find('span', class_='disc-trait difficulty has-tip tip-right radius').get_text(strip=True)
                speed = disc.find('span', class_='disc-trait speed has-tip tip-right radius').get_text(strip=True)
                glide = disc.find('span', class_='disc-trait glide has-tip tip-right radius').get_text(strip=True)
                turn = disc.find('span', class_='disc-trait hss has-tip tip-right radius').get_text(strip=True)
                fade = disc.find('span', class_='disc-trait lss has-tip tip-right radius').get_text(strip=True)
                company_name = c
                speed_int = int(speed)
                if speed_int <= 3:
                    disc_type = 'putter'
                if speed_int > 3 and speed_int <= 5:
                    disc_type = 'mid'
                if speed_int > 5 and speed_int <= 8:
                    disc_type = 'fairway'
                if speed_int > 8:
                    disc_type = 'driver'
                new_d = Disc(name=name, plastic=plastic, disc_type=disc_type, difficulty=float(difficulty), speed=float(speed), 
                            glide=float(glide), turn=float(turn), fade=float(fade), 
                            image_url=img, company_name=company_name)

                db.session.add(new_d)
                db.session.commit()
                counter += 1

            except Exception as e:
                db.session.rollback()
                print(e)
                continue


print(counter)