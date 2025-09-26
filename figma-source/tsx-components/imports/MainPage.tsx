import svgPaths from "./svg-5e2fruoy3c";
import imgImage1 from "figma:asset/0eda663dbbe179e51356aaf6447a61c336255e26.png";

function RightSide() {
  return (
    <div className="absolute h-[11.336px] right-[14.67px] top-[17.33px] w-[66.662px]" data-name="Right Side">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 67 12">
        <g id="Right Side">
          <g id="Battery">
            <path d={svgPaths.p12384570} id="Rectangle" opacity="0.35" stroke="var(--stroke-0, black)" />
            <path d={svgPaths.p1a0c9260} fill="var(--fill-0, black)" id="Combined Shape" opacity="0.4" />
            <path d={svgPaths.p2be35b00} fill="var(--fill-0, black)" id="Rectangle_2" />
          </g>
          <path d={svgPaths.p384fdc00} fill="var(--fill-0, black)" id="Wifi" />
          <path d={svgPaths.p39aee700} fill="var(--fill-0, black)" id="Mobile Signal" />
        </g>
      </svg>
    </div>
  );
}

function Time() {
  return (
    <div className="absolute h-[21px] left-[21px] top-[12px] w-[54px]" data-name="Time">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 54 21">
        <g id="Time">
          <g id="9:41">
            <path d={svgPaths.p3de63e00} fill="var(--fill-0, black)" />
            <path d={svgPaths.p3029a300} fill="var(--fill-0, black)" />
            <path d={svgPaths.p2e0c43c0} fill="var(--fill-0, black)" />
            <path d={svgPaths.p38350600} fill="var(--fill-0, black)" />
          </g>
        </g>
      </svg>
    </div>
  );
}

function LeftSide() {
  return (
    <div className="absolute contents left-[21px] top-[12px]" data-name="Left Side">
      <Time />
    </div>
  );
}

function StatusBar() {
  return (
    <div className="absolute h-[44px] left-0 overflow-clip top-0 w-[375px]" data-name="Status Bar">
      <RightSide />
      <LeftSide />
    </div>
  );
}

function IconTabHomeFill() {
  return (
    <div className="relative shrink-0 size-[24px]" data-name="Icon_Tab/Home_Fill">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 24 24">
        <g id="Icon_Tab/Home_Fill">
          <path clipRule="evenodd" d={svgPaths.pee438f0} fill="var(--fill-0, black)" fillRule="evenodd" id="home_fill" />
        </g>
      </svg>
    </div>
  );
}

function TabBarItem() {
  return (
    <div className="absolute box-border content-stretch flex gap-[10px] items-start justify-start pb-[8px] pt-[12px] px-[26px] top-0 translate-x-[-50%]" data-name="Tab Bar Item" style={{ left: "calc(50% - 150.5px)" }}>
      <IconTabHomeFill />
    </div>
  );
}

function TabBarItem1() {
  return <div className="absolute h-[44px] top-0 translate-x-[-50%] w-[76px]" data-name="Tab Bar Item" style={{ left: "calc(50% - 74.5px)" }} />;
}

function IconMenu() {
  return (
    <div className="relative shrink-0 size-[24px]" data-name="Icon/Menu">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 24 24">
        <g id="Icon/Menu">
          <path clipRule="evenodd" d={svgPaths.p175d4b00} fill="var(--fill-0, black)" fillRule="evenodd" id="Line" />
          <path clipRule="evenodd" d={svgPaths.pa7b1d00} fill="var(--fill-0, black)" fillRule="evenodd" id="Line_2" />
          <path clipRule="evenodd" d={svgPaths.p28ac8200} fill="var(--fill-0, black)" fillRule="evenodd" id="Line_3" />
        </g>
      </svg>
    </div>
  );
}

function TabBarItem2() {
  return (
    <div className="absolute box-border content-stretch flex gap-[10px] items-start justify-start pb-[8px] pt-[12px] px-[26px] top-0 translate-x-[-50%]" data-name="Tab Bar Item" style={{ left: "calc(50% + 8.5px)" }}>
      <IconMenu />
    </div>
  );
}

function IconPerson() {
  return (
    <div className="relative shrink-0 size-[24px]" data-name="Icon/Person">
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 24 24">
        <g id="Icon/Person">
          <path d={svgPaths.p3d834a00} fill="var(--fill-0, black)" id="person" />
        </g>
      </svg>
    </div>
  );
}

function TabBarItem3() {
  return (
    <div className="absolute box-border content-stretch flex gap-[10px] items-start justify-start pb-[8px] pt-[12px] px-[26px] top-[3px] translate-x-[-50%]" data-name="Tab Bar Item" style={{ left: "calc(50% + 149.5px)" }}>
      <IconPerson />
    </div>
  );
}

function Tabs() {
  return (
    <div className="absolute h-[44px] left-px overflow-clip right-[-1px] top-0" data-name="Tabs">
      <TabBarItem />
      <TabBarItem1 />
      <TabBarItem2 />
      <TabBarItem3 />
    </div>
  );
}

function HomeIndicator() {
  return (
    <div className="absolute bottom-0 h-[34px] left-1/2 translate-x-[-50%] w-[375px]" data-name="Home Indicator">
      <div className="absolute bg-black bottom-[8px] h-[5px] rounded-[100px] translate-x-[-50%] w-[134px]" data-name="Home Indicator" style={{ left: "calc(50% + 0.5px)" }} />
    </div>
  );
}

function TabBar() {
  return (
    <div className="absolute backdrop-blur-[10px] backdrop-filter bg-white h-[78px] left-0 shadow-[0px_-0.5px_0px_0px_rgba(0,0,0,0.1)] top-[734px] w-[375px]" data-name="Tab Bar">
      <Tabs />
      <HomeIndicator />
    </div>
  );
}

export default function MainPage() {
  return (
    <div className="bg-white relative size-full" data-name="main page">
      <StatusBar />
      <TabBar />
      <div className="absolute font-['Inter:Semi_Bold',_'Noto_Sans_KR:Bold',_sans-serif] font-semibold leading-[0] left-[192px] not-italic text-[24px] text-black text-center text-nowrap top-[223px] tracking-[-0.48px] translate-x-[-50%]">
        <p className="leading-[1.4] whitespace-pre">“ n시간동안 주차할 주차장 찾아줘”</p>
      </div>
      <div className="absolute bg-center bg-cover bg-no-repeat left-[12px] size-[350px] top-[289px]" data-name="image 1" style={{ backgroundImage: `url('${imgImage1}')` }} />
    </div>
  );
}