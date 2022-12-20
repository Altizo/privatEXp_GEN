import os
import rsatool.rsatool as rsatool
import configparser


config = configparser.ConfigParser()
config.read('.env')

modulus = config['rsa_data']['MODULUS']
hex_start = config['rsa_data']['START_D']
publicExponent = config['rsa_data']['PUBLIC_EXP']
start_range = config['enum_var']['START']
end_range = config['enum_var']['END']      


clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


class CALC_KEY(rsatool.RSA):
    def __init__(self):
        self.d = None
        self.e = publicExponent
        self.n = modulus
        self.hex_start = hex_start
        

    def toHex(self,dec):
        digits = '0123456789ABCDEF'
        x = (dec % 16)
        rest = dec // 16
        if (rest == 0):
            return digits[x]
        return self.toHex(rest) + digits[x]


    def gen_d(self):
        hex_d_array = []
        for variant in range(int(start_range),int(end_range),1):
            hex_end = (self.toHex(int(variant)))
            hex=self.hex_start+hex_end
            hex_d_array.append(int(hex,16))
        return hex_d_array
        

    def search_d(self):
        array_d = self.gen_d()
        for step, hex_d in enumerate(self.gen_d()):
            clearConsole()
            print('{}/{}        {}'.format(step+1,len(array_d),str(hex_d)[:7]+'...'+str(hex_d)[len(str(hex_d))-7:]))
            try:
                answer = rsatool.factor_modulus(d=int(hex_d),n=int(self.n), e=int(self.e))
                self.d = hex_d
                print('-----------------XE-XE-XE-XE------------------privateExponent-d---')
                print(hex_d)
                print('----------------------------------------------prime1-p------------')
                print(answer[0])
                print('----------------------------------------------prime2-q------------')
                print(answer[1])
                print('------------------------------------------------------------------')
                break
            except:
                pass
        if self.d==None:
            clearConsole()
            print('-------SEARCH COMPLETE-------\n privatExponent - NOT FOUND!')


calc_k = CALC_KEY()
calc_k.search_d()


