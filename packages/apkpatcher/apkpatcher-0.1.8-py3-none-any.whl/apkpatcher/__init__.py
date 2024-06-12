#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import os.path
import tempfile
import subprocess
import logging
from pathlib import Path

from . import conf
import pyaxml
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

def plba(filename, arch):
    p = Path(filename)
    return f"{os.path.dirname(p)}/{p.stem}_{arch}.so"

class Patcher:

    ARCH_ARM = 'arm'
    ARCH_ARM64 = 'arm64'
    ARCH_X86 = 'x86'
    ARCH_X64 = 'x64'

    DEFAULT_GADGET_NAME = 'libfrida-gadget.so'

    CONFIG_BIT = 1 << 0
    AUTOLOAD_BIT = 1 << 1

    INTERNET_PERMISSION = 'android.permission.INTERNET'

    def __init__(self, apk : str, sdktools : str, version : str):
        '''
        Initialisation of patcher

        Parameters:
                    apk (str): path of the apk
                    sdktools (str): path of the sdktools for zipalign
                    version (str): version to choose the correct path of
                    build_tools

        '''
        self.apk = apk
        self.arch = None
        self.sdktools = sdktools
        self.version = version
        self.final_dir = None
        self._pause = False
        self.plugin = None
        self.path_build_tools = f"{sdktools}/build-tools/{version}/" if \
                (sdktools and version) else ""
        self.network_certificates = []

################################################################################
#                                                                              #
#            CERTIFICATES                                                      #
#                                                                              #
################################################################################
   
    def add_network_certificate(self, cert):
        self.network_certificates.append(cert)

    def inject_custom_network_certificate(self, rsc, path_network : str):
        netsec_path = os.path.join(self.final_dir, path_network)
        ca_path = os.path.join(self.final_dir, "res/my_ca")

        ID = rsc.add_id_public(rsc.get_packages()[0],"raw", "network_security_config_ca", "res/my_ca")

        buf = f"""
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                    <certificates src="@{hex(ID)[2:]}"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """

        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())

        for cert in self.network_certificates:
            shutil.copyfile(cert, ca_path)
        logging.info("Custom certificate was injected inside the apk")
    
    def create_security_config_xml(self, path_network : str):
        netsec_path = os.path.join(self.final_dir, path_network)

        buf = """
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """
        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())


        logging.info('The network_security_config.xml file was created!')


    def enable_user_certificates(self, rsc):
        path_network = self.inject_user_certificates_label(rsc)
        if path_network:
            if self.network_certificates:
                self.inject_custom_network_certificate(rsc, path_network)
            else:
                self.create_security_config_xml(path_network)
    
    def inject_user_certificates_label(self, rsc : pyaxml.ARSC):
        logging.info('Injecting Network Security label to accept user certificates...')

        manifest_path = os.path.join(self.final_dir, 'AndroidManifest.xml')

        if not os.path.isfile(manifest_path):
            logging.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return None
        
        with open(manifest_path, 'rb') as fp:
            buf = fp.read()



            ID = rsc.get_id_public(rsc.get_packages()[0], "xml", "network_security_config")
            if not ID:
                path_network = "res/network_security_config.xml"
                ID = rsc.add_id_public(rsc.get_packages()[0],"xml", "network_security_config", path_network)
            else:
                ID, path_network = ID
                path_network = pyaxml.StringBlocks(proto=rsc.proto.stringblocks).decode_str(path_network)

            
            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            application = xml.findall("./application")[0]
            application.attrib["{http://schemas.android.com/apk/res/android}networkSecurityConfig"] = f"@{hex(ID)[2:]}"
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(xml)

            with open(manifest_path, 'wb') as fp:
                fp.write(res_aml.pack())
    
            logging.info('The Network Security label was added!')

        return path_network

    





################################################################################
#                                                                              #
#                        PERMISSIONS                                           #
#                                                                              #
################################################################################

    def has_permission(self, permission_name : str) -> bool:
        '''
        Check if the apk have 'permission_name' as permission
        
        Parameters:
                    permission_name (str): name of the permission with format:
                    android.permission.XXX

        Returns:
                has_permission (bool): permission is present
        '''
        manifest_path = os.path.join(self.final_dir, 'AndroidManifest.xml')

        if not os.path.isfile(manifest_path):
            logging.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return 

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()

            # Search over all the application permissions
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for permission in xml.findall('./uses-permission'):
                if permission.attrib[android_name] == permission_name:
                    logging.info(f"The app {self.apk} has the permission '{permission_name}'")
                    return True

        logging.info(f"The app {self.apk} doesn't have the permission '{permission_name}'")
        return False

    def inject_permission_manifest(self, permission : str):
        '''
        Inject permission on the Manifest
        '''
        logging.info(f"Injecting permission {permission} in Manifest...")

        manifest_path = os.path.join(self.final_dir, 'AndroidManifest.xml')

        if not os.path.isfile(manifest_path):
            logging.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False


        with open(manifest_path, 'rb') as fp:
            buf = fp.read()

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            res_aml = None
            for i in range(len(xml)):
                if xml[i].tag == 'application' or xml[i].tag == 'uses-permission':
                    newperm = etree.Element('uses-permission')
                    newperm.attrib['{http://schemas.android.com/apk/res/android}name'] = permission
                    xml.insert(i, newperm)
                    res_aml = pyaxml.axml.AXML()
                    res_aml.from_xml(xml)
                    break

        with open(manifest_path, 'wb') as fp:
            fp.write(res_aml.pack())
        return True


################################################################################
#                                                                              #
#                EXTRACT REPACK APK                                            #
#                                                                              #
################################################################################

    def extract_apk(self):
        '''
        Extract the apk on the temporary folder
        '''

        logging.info(f"Extracting {self.apk} (without resources) to {self.final_dir}")
        result = subprocess.check_output(" ".join(['apktool', '-f', '-r', 'd', '-o', self.final_dir , self.apk]), shell=True)
        print(result.decode('utf-8'))

    def sign_and_zipalign(self, apk_path, splits_apk):
        '''
        sign and zipalign file
        '''

        logging.info('Optimizing with zipalign...')

        tmp_target_file = apk_path.replace('.apk', '_tmp.apk')
        shutil.move(apk_path, tmp_target_file)

        subprocess.call(f"{self.path_build_tools}zipalign -p 4 {tmp_target_file} {apk_path}", stderr=subprocess.STDOUT, shell=True)

        os.remove(tmp_target_file)


        logging.info('Generating a random key...')
        subprocess.call(
            'keytool -genkey -keyalg RSA -keysize 2048 -validity 700 -noprompt -alias apkpatcheralias1 -dname '
            '"CN=apk.patcher.com, OU=ID, O=APK, L=Patcher, S=Patch, C=BR" -keystore apkpatcherkeystore '
            '-storepass password -keypass password 2> /dev/null',
            shell=True)

        logging.info('Signing the patched apk...')
        subprocess.call(
                f"{self.path_build_tools}apksigner sign --ks apkpatcherkeystore"
                f" --ks-key-alias apkpatcheralias1 --key-pass pass:password "
                f"--ks-pass pass:password --out {apk_path} {apk_path}", shell=True)

        for split in splits_apk:
            split_new_name = split.replace('.apk', '_new_signed.apk')
            subprocess.call(
                f"{self.path_build_tools}apksigner sign --ks apkpatcherkeystore"
                f" --ks-key-alias apkpatcheralias1 --key-pass pass:password "
                f"--ks-pass pass:password --out {split_new_name} {split}", shell=True)


        os.remove('apkpatcherkeystore')

        logging.info('The apk was signed!')

        logging.info('The file was optimized!')

    def pause(self, pause):
        self._pause = pause
    
    def set_plugin(self, plugin):
        self.plugin = plugin

    def repackage_apk(self, target_file=None):
        '''
        repackage the apk

        Parameters:
                    - target_file (str) : the path of the new apk created if
                      none, a new apk will be created with suffix "_patched.apk"
        '''
        if self.plugin:
            subprocess.run([self.plugin, self.final_dir])
        if self._pause:
            print(f"You can modify the apk here: {self.final_dir}")
            input()
        if target_file is None:
            current_path = os.getcwd()
            target_file = os.path.join(current_path, self.apk.replace('.apk', '_patched.apk'))

            if os.path.isfile(target_file):
                timestamp = str(time.time()).replace('.', '')
                new_file_name = target_file.replace('.apk', '_{0}.apk'.format(timestamp))
                target_file = new_file_name

        logging.info('Repackaging apk to {0}'.format(target_file))
        logging.info('This may take some time...')

        subprocess.check_output(" ".join(['apktool', 'b', '-o', target_file, self.final_dir]), shell=True)

        return target_file


################################################################################
#                                                                              #
#                INJECT NATIVE CODE                                            #
#                                                                              #
################################################################################

    def get_entrypoint_class_name(self):
        '''
        get the class name of the entrypoint
        '''
        entrypoint_class = None
        manifest_path = os.path.join(self.final_dir, 'AndroidManifest.xml')

        if not os.path.isfile(manifest_path):
            logging.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return 

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()
            # Look over all the activities and try to find either one with MAIN as action or LAUNCHER as category 
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for activity in xml.findall('./application/activity'):
                for action in activity.findall('intent-filter/action'):
                    if action.attrib[android_name] == 'android.intent.action.MAIN':
                        entrypoint_class = activity.attrib[android_name]
                        break
                for category in activity.findall('intent-filter/category'):
                    if category.attrib[android_name] == 'android.intent.category.LAUNCHER':
                        entrypoint_class = activity.attrib[android_name]
                        break

            # Do the same for activities alias in case we did not find the main activity
            if not entrypoint_class:
                android_target_activity = "{http://schemas.android.com/apk/res/android}targetActivity"
                for alias in xml.findall('./application/activity-alias'):
                    for action in alias.findall('intent-filter/action'):
                        if action.attrib[android_name] == 'android.intent.action.MAIN':
                            entrypoint_class = alias.attrib[android_target_activity]
                            break
                    for category in alias.findall('intent-filter/category'):
                        if category.attrib[android_name] == 'android.intent.category.LAUNCHER':
                            entrypoint_class = alias.attrib[android_target_activity]
                            break

            # Check if entry point is relative, if so search in the Manifest package
            if entrypoint_class.startswith('.'):
                entrypoint_class = xml.attrib['package'] + entrypoint_class

        if entrypoint_class is None:
            logging.error('Fail to find entrypoint class')

        return entrypoint_class

    def get_entrypoint_smali_path(self):
        '''
        get the path of apk entrypoint on the smali files
        '''
        files_at_path = os.listdir(self.final_dir)
        entrypoint_final_path = None

        for file in files_at_path:
            if file.startswith('smali'):
                entrypoint_tmp = os.path.join(self.final_dir, file, self.entrypoint_class.replace('.', '/') + '.smali')
                if os.path.isfile(entrypoint_tmp):
                    entrypoint_final_path = entrypoint_tmp
                    break

        if entrypoint_final_path is None:
            logging.error('Couldn\'t find the application entrypoint')
            sys.exit(1)
        else:
            logging.info('Found application entrypoint at {0}'.format(entrypoint_final_path))

        return entrypoint_final_path

    def insert_frida_loader(self, frida_lib_name='frida-gadget'):
        '''
        inject snippet to load frida-gadget in smali code
        '''
        partial_injection_code = '''
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

        '''.replace('<LIBFRIDA>', frida_lib_name)

        full_injection_code = '''
.method static constructor <clinit>()V
    .locals 1

    .prologue
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void
.end method
        '''.replace('<LIBFRIDA>', frida_lib_name)

        with open(self.entrypoint_smali_path, 'r') as smali_file:
            content = smali_file.read()

            if 'frida-gadget' in content:
                logging.info('The frida-gadget is already in the entrypoint. Skipping...')
                return False

            direct_methods_start_index = content.find('# direct methods')
            direct_methods_end_index = content.find('# virtual methods')

            if direct_methods_start_index == -1 and direct_methods_end_index == -1:
                logging.error('Could not find direct methods.')
                return False

            class_constructor_start_index = content.find('.method static constructor <clinit>()V',
                    direct_methods_start_index, direct_methods_end_index)

            if class_constructor_start_index == -1:
                has_class_constructor = False
            else:
                has_class_constructor = True

            class_constructor_end_index = -1
            if has_class_constructor:
                class_constructor_end_index = content.find('.end method',
                        class_constructor_start_index, direct_methods_end_index)

                if has_class_constructor and class_constructor_end_index == -1:
                    logging.error('Could not find the end of class constructor.')
                    return False

            prologue_start_index = -1
            if has_class_constructor:
                prologue_start_index = content.find('.prologue',
                        class_constructor_start_index, class_constructor_end_index)

            no_prologue_case = False
            locals_start_index = -1
            if has_class_constructor and prologue_start_index == -1:
                no_prologue_case = True

                locals_start_index = content.find('.locals ',
                        class_constructor_start_index, class_constructor_end_index)

                if no_prologue_case and locals_start_index == -1:
                    logging.error('Has class constructor. No prologue case, but no "locals 0" found.')
                    return False

            locals_end_index = -1
            if no_prologue_case:
                locals_end_index = locals_start_index + len('locals X')

            prologue_end_index = -1
            if has_class_constructor and prologue_start_index > -1:
                prologue_end_index = prologue_start_index + len('.prologue') + 1

            if has_class_constructor:
                if no_prologue_case:
                    new_content = content[0:locals_end_index]

                    if content[locals_end_index] == '0':
                        new_content += '1'
                    else:
                        new_content += content[locals_end_index]

                    new_content += '\n\n    .prologue'
                    new_content += partial_injection_code
                    new_content += content[locals_end_index+1:]
                else:
                    new_content = content[0:prologue_end_index]
                    new_content += partial_injection_code
                    new_content += content[prologue_end_index:]
            else:
                tmp_index = direct_methods_start_index + len('# direct methods') + 1
                new_content = content[0:tmp_index]
                new_content += full_injection_code
                new_content += content[tmp_index:]

        # The newContent is ready to be saved

        with open(self.entrypoint_smali_path, 'w') as smali_file:
            smali_file.write(new_content)

        logging.info('Frida loader was injected in the entrypoint smali file!')

        return True

    def create_lib_arch_folders(self, arch):
        '''
        make lib folder in the apk to put native lib
        '''
        # noinspection PyUnusedLocal
        sub_dir = None
        sub_dir_2 = None

        libs_path = os.path.join(self.final_dir, 'lib/')

        if not os.path.isdir(libs_path):
            logging.info('There is no "lib" folder. Creating...')
            os.makedirs(libs_path)

        if arch == self.ARCH_ARM:
            sub_dir = os.path.join(libs_path, 'armeabi')
            sub_dir_2 = os.path.join(libs_path, 'armeabi-v7a')

        elif arch == self.ARCH_ARM64:
            sub_dir = os.path.join(libs_path, 'arm64-v8a')

        elif arch == self.ARCH_X86:
            sub_dir = os.path.join(libs_path, 'x86')

        elif arch == self.ARCH_X64:
            sub_dir = os.path.join(libs_path, 'x86_64')

        else:
            logging.error("Couldn't create the appropriate folder with the given arch.")
            return []

        if not os.path.isdir(sub_dir):
            logging.info('Creating folder {0}'.format(sub_dir))
            os.makedirs(sub_dir)

        if arch == self.ARCH_ARM:
            if not os.path.isdir(sub_dir_2):
                logging.info('Creating folder {0}'.format(sub_dir_2))
                os.makedirs(sub_dir_2)

        if arch == self.ARCH_ARM:
            return [sub_dir, sub_dir_2]

        else:
            return [sub_dir]

    def check_libextract(self):
        logging.info('check if lib is extractable')

        manifest_path = os.path.join(self.final_dir, 'AndroidManifest.xml')

        if not os.path.isfile(manifest_path):
            logging.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False


        with open(manifest_path, 'rb') as fp:
            axml, _ = pyaxml.AXML.from_axml(fp.read())
            etree = axml.to_xml()
            extractNative = etree.findall("./application/[@{http://schemas.android.com/apk/res/android}extractNativeLibs='false']")
            if len(extractNative) > 0:
                extractNative[0].attrib['{http://schemas.android.com/apk/res/android}extractNativeLibs'] = 'true'

        with open(manifest_path, 'wb') as fp:
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(etree)
            fp.write(res_aml.pack())


    def insert_frida_lib(self, gadget_path : str, arch : str, config_file_path=None, auto_load_script_path=None):
        '''
        Insert native lib inside the apk

        Parameters:
                    - gadget_path (str): the path of the gadget to insert
        '''
        arch_folders = self.create_lib_arch_folders(arch)

        if not arch_folders:
            logging.error('Some error occurred while creating the libs folders')
            return False

        for folder in arch_folders:
            if config_file_path and auto_load_script_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.CONFIG_BIT | self.AUTOLOAD_BIT)

            elif config_file_path and not auto_load_script_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.CONFIG_BIT)

            elif auto_load_script_path and not config_file_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.AUTOLOAD_BIT)

            else:
                self.delete_existing_gadget(folder, delete_custom_files=0)

            target_gadget_path = os.path.join(folder, self.DEFAULT_GADGET_NAME)

            logging.info(f"Copying gadget to {target_gadget_path}")

            shutil.copyfile(gadget_path, target_gadget_path)

            if config_file_path:
                target_config_path = target_gadget_path.replace('.so', '.config.so')

                logging.info("Copying config file to {target_config_path}")
                shutil.copyfile(config_file_path, target_config_path)

            if auto_load_script_path:
                target_autoload_path = target_gadget_path.replace(self.DEFAULT_GADGET_NAME, self.DEFAULT_HOOKFILE_NAME)

                logging.info("Copying auto load script file to {target_autoload_path}")
                shutil.copyfile(auto_load_script_path, target_autoload_path)

        return True
    
    def delete_existing_gadget(self, arch_folder, delete_custom_files=0):
        '''
        delete existing gadget inside the apk
        '''
        gadget_path = os.path.join(arch_folder, self.DEFAULT_GADGET_NAME)

        if os.path.isfile(gadget_path):
            os.remove(gadget_path)

        if delete_custom_files & self.CONFIG_BIT:
            config_file_path = os.path.join(arch_folder, self.DEFAULT_CONFIG_NAME)

            if os.path.isfile(config_file_path):
                os.remove(config_file_path)

        if delete_custom_files & self.AUTOLOAD_BIT:
            hookfile_path = os.path.join(arch_folder, self.DEFAULT_HOOKFILE_NAME)

            if os.path.isfile(hookfile_path):
                os.remove(hookfile_path)
    






################################################################################
#                                                                              #
#                PATCHING                                                      #
#                                                                              #
################################################################################


    def set_arch(self, arch):
        self.arch = arch


    def patching(self, gadget_to_use=None, output_file=None, user_certificate=False, splits_apk=[]):
        '''
        patch the apk with gadget 'gadget_to_use'
        '''
        if len(self.network_certificates) > 0:
            user_certificate = True
        if not os.path.isfile(self.apk):
            logging.error(f"The file {self.apk} couldn't be found!")
            sys.exit(1)

        # Create tempory file
        with tempfile.TemporaryDirectory() as tmp_dir:
            apk_name = Path(self.apk).stem
            self.final_dir = f"{tmp_dir}/{apk_name}"

            # extract the apk on temporary folder
            self.extract_apk()

            # add Internet permission
            has_internet_permission = self.has_permission(self.INTERNET_PERMISSION)
            if not has_internet_permission:
                if not self.inject_permission_manifest(self.INTERNET_PERMISSION):
                    sys.exit(1)

            # add users certificate
            if user_certificate:
                with open(f"{self.final_dir}/resources.arsc", "r+b") as fp:
                    rsc, _ = pyaxml.ARSC.from_axml(fp.read())
                    self.enable_user_certificates(rsc)
                    rsc.compute()
                    fp.seek(0)
                    fp.write(rsc.pack())


            # inject frida library
            self.entrypoint_class = self.get_entrypoint_class_name()
            self.entrypoint_smali_path = self.get_entrypoint_smali_path()
            if gadget_to_use:
                self.insert_frida_loader()
            self.check_libextract()

            if gadget_to_use:
                if not self.arch:
                    archs = [(plba(gadget_to_use, self.ARCH_ARM),  self.ARCH_ARM),
                            (plba(gadget_to_use, self.ARCH_ARM64), self.ARCH_ARM64),
                            (plba(gadget_to_use, self.ARCH_X86),   self.ARCH_X86),
                            (plba(gadget_to_use, "x86_64"),   self.ARCH_X64)]
                else:
                    archs = [(gadget_to_use, self.arch)]
                for gadget, arch in archs:
                    self.insert_frida_lib(gadget, arch)

            # repackage the apk and sign + align it
            if output_file:
                output_file_path = self.repackage_apk(target_file=output_file)

            else:
                output_file_path = self.repackage_apk()

            self.sign_and_zipalign(output_file_path, splits_apk)




    @staticmethod
    def get_default_config_file():
        config = '''
{
    "interaction": {
        "type": "script",
        "address": "127.0.0.1",
        "port": 27042,
        "path": "./libhook.js.so"
    }
}
        '''

        path = os.path.join(os.getcwd(), 'generatedConfigFile.config')
        f = open(path, 'w')

        f.write(config)
        f.close()

        return path






if __name__ == '__main__':
    main()

